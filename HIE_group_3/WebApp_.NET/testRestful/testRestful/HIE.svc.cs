using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;
using System.Web;
using System.Web.Helpers;
using System.Net.Mail;
using System.Net.Mime;
using MySql.Data.MySqlClient;

namespace testRestful
{
    public class ClinicalSummary : IClinicalSummary
    {
        //Uses the Greenway ClinicalSummaryGet to retrieve the CCD
        public String GetClinicalSummary(String PatientID)
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(reqHdrJsonStr);
            sb.Remove(reqHdrJsonStr.Length - 1, 1);
            sb.Append("\"PatientID\":" + PatientID);
            sb.Append("}");

            object response = MakeRequest(ClinicalSummaryGetURL, sb.ToString(), typeof(ClinicalSummaryResponse));
            ClinicalSummaryResponse res = response as ClinicalSummaryResponse;
            StringWriter sw = new StringWriter();
            if (res != null)
            {
                HttpUtility.HtmlDecode(res.Data,sw);
                return sw.ToString();
            }
            else
            {
                return response.ToString();
            }
        }

        // Uses Greenway PatientMedicationGet
        public String GetMedication(String PatientID)
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(reqHdrJsonStr);
            sb.Remove(reqHdrJsonStr.Length - 1, 1);
            sb.Append("\"PatientID\":" + PatientID);
            sb.Append("}");

            object response = MakeRequest(MedicationGetURL, sb.ToString(), typeof(Medications));
            Medications res = response as Medications;
            StringWriter sw = new StringWriter();
            if (res != null)
            {
                //Push the retrieved data into the shared repo
                String connstr = "Server=hit4.nimbus.cip.gatech.edu;Database=healthit;Uid=group3;Pwd=group3";
                MySqlConnection conn = new MySqlConnection(connstr);
                MySqlCommand cmd;
                conn.Open();
                try
                {
                    for (int i = 0; i < res.PatientMedictions.Count; i++)
                    {
                        Medication med = res.PatientMedictions[i].Medication;
                        cmd = conn.CreateCommand();
                        cmd.CommandText = "INSERT INTO `healthit`.`medications`(`patientid`,`medicationid`,`medname`,`medstrength`,`medstrengthunit`,`doseform`,`dispenseamnt`,`sig`,`startdate`,`expirydate`)" +
                            "VALUES(@patientid,@medicationid,@medname,@medstrength,@medstrengthunit,@doseform,@dispenseamnt,@sig,@startdate,@expirydate);";
                        cmd.Parameters.AddWithValue("@patientid",PatientID);
                        cmd.Parameters.AddWithValue("@medicationid",med.MedicationId);
                        cmd.Parameters.AddWithValue("@medname",med.MedicationName);
                        cmd.Parameters.AddWithValue("@medstrength",med.MedicationStrength);
                        cmd.Parameters.AddWithValue("@medstrengthunit",med.MedicationStrengthUnit);
                        cmd.Parameters.AddWithValue("@doseform",med.DoseForm);
                        cmd.Parameters.AddWithValue("@dispenseamnt",med.DispenseAmount);
                        cmd.Parameters.AddWithValue("@sig",med.SIG);
                        cmd.Parameters.AddWithValue("@startdate",res.PatientMedictions[i].DateStarted);
                        cmd.Parameters.AddWithValue("@expirydate", res.PatientMedictions[i].ExpiredDate);
                        cmd.ExecuteNonQuery();

                    }
                    
                }
                catch (Exception e)
                {
                    sw.Write(e.Message+ e.StackTrace);
                }
                finally
                {
                    if (conn.State == System.Data.ConnectionState.Open)
                        conn.Close();
                }

                return sw.ToString();
            }
            else
            {
                return response.ToString();
            }
        }

        public String SendReport(String PatientID, String Base64Document, String DocumentName){

            return SendReport(PatientID, Base64Document, DocumentName, "4", "15");
        }

        // Uses Greenway DocumentImportChart
        public String SendReport(String PatientID, String Base64Document, String DocumentName, String DocumentFileType, String DocumentTypeID)
        {
            if (DocumentFileType == null)
                DocumentFileType = "4";
            if (DocumentTypeID == null)
                DocumentTypeID = "17";
            StringBuilder sb = new StringBuilder();
            sb.Append(reqHdrJsonStr);
            sb.Remove(reqHdrJsonStr.Length - 1, 1);
            sb.Append("\"Base64Document\":\"" + Base64Document + "\", ");
            sb.Append("\"DocumentFileType\":"+DocumentFileType+", ");
            sb.Append("\"DocumentName\":\"" + DocumentName + "\", ");
            sb.Append("\"DocumentDescription\": \""+ DocumentName +"\",");
            sb.Append("\"DocumentTypeID\": " + DocumentTypeID + ",");
            sb.Append("\"PrimeSuitePatientId\":" + PatientID);

            sb.Append("}");

            object response = MakeRequest(DocumentImportURL, sb.ToString(), null);
            
            return response.ToString();
        }

        //Uses patient sendmsg
        public String SendMessage(String PatientID, String RecipientID, String Subject, String Body, String Priority)
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(reqHdrJsonStr);
            sb.Remove(reqHdrJsonStr.Length - 1, 1);
            sb.Append("\"AddToChart\":true,");
            sb.Append("\"DocumentID\":0,");
            sb.Append("\"Message\":{ \"Body\":\""+Body+"\",");
            sb.Append("\"FromUserID\":1,\"FromUserName\":\"admin\",");
            sb.Append("\"MessageRecipient\":{ \"Recipients\":[{ \"RecipientID\":" + RecipientID + ",\"Type\": \"user\"}]},");
            sb.Append("\"PatientID\":" + PatientID + ", ");
            sb.Append("\"Priority\":" + "1" + ", ");
            sb.Append("\"Subject\":\"" + Subject + "\", ");
            sb.Append("\"Type\":1004},\"PatientInfo\":{");
            sb.Append("\"PatientID\":" + PatientID + ", ");
            sb.Append("\"ResidentialAddress\":{}}");
            sb.Append("}");

            object response = MakeRequest(MessageSaveURL, sb.ToString(), null);
            
            return response.ToString();
            
        }

        
        public static object MakeRequest(String requestUrl,String json,Type type)
        {
            HttpWebResponse response = null;
            try
            {
                HttpWebRequest request = WebRequest.Create(requestUrl) as HttpWebRequest;
                
                request.ContentType = "text/json";
                request.Method = "POST";
                using (var streamWriter = new StreamWriter(request.GetRequestStream()))
                {
                    streamWriter.Write(json);
                    streamWriter.Flush();
                    streamWriter.Close();
                    using (response = request.GetResponse() as HttpWebResponse)
                    {
                       
                        if (type != null)
                        {

                            DataContractJsonSerializer jsonSerializer = new DataContractJsonSerializer(type);
                            object objResponse = jsonSerializer.ReadObject(response.GetResponseStream());
                            return objResponse;
                        }
                       
                        StreamReader sr = new StreamReader(response.GetResponseStream());
                        return sr.ReadToEnd();
                        
                    }
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                return e.Message + e.Source + e.StackTrace;
            }
        }

        private static String API_URL = "https://api-test.greenwaymedical.com/Integration/RESTv1.0/PrimeSuiteAPIService/";
        private static String API_KEY = "gxzzfraga2uunq2mj6s79zdx";
        private static String ClinicalSummaryGetURL = API_URL + "Patient/ClinicalSummaryGet?api_key=" + API_KEY;
        private static String MedicationGetURL = API_URL + "Patient/PatientMedicationGet?api_key=" + API_KEY;
        private static String DocumentImportURL = API_URL + "Document/DocumentImportChart?api_key=" + API_KEY;
        private static String MessageSaveURL = API_URL + "Messaging/MessageSend?api_key=" + API_KEY;
        private String reqHdrJsonStr = "{" +
          "\"CDADocumentType\":1001,"+
          "\"CDAProfile\":{" +
                    "\"ProfileType\":0," +
                    "\"VisitId\":[0]" +
          "}," +
          "\"Credentials\":{" +
                    "\"PrimeSuiteCredential\":{" +
                             "\"PrimeSuiteSiteId\":\"APIDemo\"," +
                              "\"PrimeSuiteUserAlias\":\"\"," +
                              "\"PrimeSuiteUserName\":\"admin\"," +
                              "\"PrimeSuiteUserPassword\":\"password\"" +
                    "}," +
                    "\"VendorCredential\":{" +
                              "\"VendorLogin\":\"GeorgiaTechGUID\"," +
                              "\"VendorPassword\":\"GeorgiaTechGUID\"" +
                    "}" +
          "}," +
          "\"Header\":{" +
                    "\"DestinationSiteID\":\"APIDemo\"," +
                    "\"PrimeSuiteUserID\":1," +
                    "\"SourceSiteID\":\"\"" +
          "},}";
    }

    public class PrimeSuiteCredential
    {
        public String PrimeSuiteSiteId { get; set; }
        public String PrimeSuiteUserAlias { get; set; }
        public String PrimeSuiteUserName { get; set; }
        public String PrimeSuiteUserPassword { get; set; }
    }

    public class VendorCredential
    {
        public String VendorLogin { get; set; }
        public String VendorPassword { get; set; }
    }

    public class Credentials
    {
        public PrimeSuiteCredential PrimeSuiteCredential { get; set; }
        public VendorCredential VendorCredential { get; set; }
    }

    public class Header
    {
        public String DestinationSiteID { get; set; }
        public int PrimeSuiteUserID { get; set; }
        public String SourceSiteID { get; set; }
    }

    public class Group
    {
        public int GroupType { get; set; }
        public String UsersHtmList { get; set; }
    }

    public class Recipient
    {
        public String DisplayText { get; set; }
        public String Name { get; set; }
        public int RecipientID { get; set; }
        public String Type { get; set; }
        public Group Group { get; set; }
    }

    public class MessageRecipient
    {
        public List<Recipient> Recipients { get; set; }
    }

    public class Message
    {
        public String Body { get; set; }
        public int Folder { get; set; }
        public int FromUserID { get; set; }
        public String FromUserName { get; set; }
        public String FullName { get; set; }
        public int MessageID { get; set; }
        public MessageRecipient MessageRecipient { get; set; }
        public int PatientID { get; set; }
        public int Priority { get; set; }
        public int ReadStatus { get; set; }
        public DateTime ReceivedDate { get; set; }
        public String Subject { get; set; }
        public int Type { get; set; }
        public String TypeDescription { get; set; }
    }

    public class ResidentialAddress
    {
        public int AddressID { get; set; }
        public String AddressLine1 { get; set; }
        public String AddressLine2 { get; set; }
        public String City { get; set; }
        public int Country { get; set; }
        public String County { get; set; }
        public String FaxNumber { get; set; }
        public String PhoneNumber1 { get; set; }
        public String PhoneNumber2 { get; set; }
        public String PostalCode { get; set; }
        public int State { get; set; }
    }

    public class PatientInfo
    {
        public String Age { get; set; }
        public DateTime DateOfBirth { get; set; }
        public String FullName { get; set; }
        public int Gender { get; set; }
        public int Legacy { get; set; }
        public String OtherID { get; set; }
        public int PatientID { get; set; }
        public String PrimaryPhoneNumber { get; set; }
        public ResidentialAddress ResidentialAddress { get; set; }
        public String SSN { get; set; }
    }

    public class RootObject
    {
        public Credentials Credentials { get; set; }
        public Header Header { get; set; }
        public bool AddToChart { get; set; }
        public int DocumentID { get; set; }
        public Message Message { get; set; }
        public PatientInfo PatientInfo { get; set; }
    }

    public class ClinicalSummaryResponse
    {
        public String Data { get; set; }
        public String ExtractDateTime { get; set; }
    }

    public class DocumentImportResponse
    {
        public int DocumentID { get; set; }
        public String DocumentImporErrorStatus { get; set; }
        public String DocumentImportStatus { get; set; }
    }

    public class Medication
    {
        public int ActionID { get; set; }
        public int AdministeredInOffice { get; set; }
        public object Calculate { get; set; }
        public int Class1 { get; set; }
        public string DEACode { get; set; }
        public string DispenseAmount { get; set; }
        public int DispenseAsWritten { get; set; }
        public string DispenseUnit { get; set; }
        public object Dosage { get; set; }
        public string DosageUnits { get; set; }
        public string DoseForm { get; set; }
        public int DoseFormID { get; set; }
        public string DoseQuantity { get; set; }
        public string DoseRoute { get; set; }
        public int DoseRouteID { get; set; }
        public int DoseUnitID { get; set; }
        public object DrugName { get; set; }
        public string DrugNameID { get; set; }
        public string Duration { get; set; }
        public string DurationUnit { get; set; }
        public int DurationUnitID { get; set; }
        public int External { get; set; }
        public object FreqDescription { get; set; }
        public string FrequencyCode { get; set; }
        public int GCNSeqNo { get; set; }
        public object HowOftenTaken { get; set; }
        public object HowTaken { get; set; }
        public object IndAvail { get; set; }
        public int InterUnitID { get; set; }
        public int Interval { get; set; }
        public int MEDID { get; set; }
        public object MNID { get; set; }
        public string Maintenance { get; set; }
        public object ManExist { get; set; }
        public string MedicationDescription { get; set; }
        public int MedicationId { get; set; }
        public string MedicationName { get; set; }
        public string MedicationStrength { get; set; }
        public string MedicationStrengthUnit { get; set; }
        public string NameType { get; set; }
        public int Notify { get; set; }
        public int NotifyCareProviderID { get; set; }
        public int NotifyCareProviderID2 { get; set; }
        public string NumRefills { get; set; }
        public int OSID { get; set; }
        public int OptionNumber { get; set; }
        public object Prospective { get; set; }
        public int RMID { get; set; }
        public object Route { get; set; }
        public int RouteID { get; set; }
        public string SIG { get; set; }
        public int SIGModeID { get; set; }
        public int SampleGiven { get; set; }
        public object ShowDuration { get; set; }
        public int StatusID { get; set; }
        public object UseForm { get; set; }
        public int uid { get; set; }
    }

    public class PatientMediction
    {
        public String DateStarted { get; set; }
        public String ExpiredDate { get; set; }
        public Medication Medication { get; set; }
        public int OrderingDocumentID { get; set; }
        public int OriginalPatientMedicationID { get; set; }
        public int PatientMedicationId { get; set; }
        public string SIG { get; set; }
    }

    public class Medications
    {
        public List<PatientMediction> PatientMedictions { get; set; }
    }

}
