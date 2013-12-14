using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

namespace testRestful
{
    // NOTE: You can use the "Rename" command on the "Refactor" menu to change the interface name "IService1" in both code and config file together.
    [ServiceContract]
    public interface IClinicalSummary
    {
        
        [OperationContract]
        [WebGet(BodyStyle=WebMessageBodyStyle.WrappedRequest,
            ResponseFormat = WebMessageFormat.Json)]
        String GetClinicalSummary(String PatientID);

        [OperationContract]
        [WebGet(BodyStyle = WebMessageBodyStyle.WrappedRequest,
            ResponseFormat = WebMessageFormat.Json)]
        String GetMedication(String PatientID);

        [OperationContract]
        [WebInvoke(RequestFormat = WebMessageFormat.Json, BodyStyle = WebMessageBodyStyle.WrappedRequest,
            ResponseFormat = WebMessageFormat.Json, Method = "POST")]
        String SendReport(String PatientID, String Base64Document, String DocumentName,String DocumentFileType, String DocumentTypeID);

        [OperationContract]
        [WebInvoke(RequestFormat = WebMessageFormat.Json, BodyStyle=WebMessageBodyStyle.WrappedRequest,
            ResponseFormat = WebMessageFormat.Json, Method = "POST")]
        String SendMessage(string PatientID, string RecipientID, string Subject, string Body, string Priority);

    }

}
