//
//  ViewController.m
//  ActivityMonitor
//
//  Created by Rob Stevenson on 9/30/13.
//  Copyright (c) 2013 Rob Stevenson. All rights reserved.
//

#import "ViewController.h"
#import <CoreMotion/CoreMotion.h>
#import "Activity.h"
#import "StepDay.h"
#import "Reachability.h"

@interface ViewController ()
{

@private
   CMMotionActivityManager *manager;
   CMStepCounter *counter;
   NSDate *curDay;
   int dayOffset;
   NSMutableArray *activityData;
   NSMutableArray *stepData;
   NSURLConnection *sendStepsCon;
   NSURLConnection *sendActCon;
   NSString *host;
   NSDateFormatter *dispFormat;
    BOOL currentlySending;
}
@end

@implementation ViewController

- (void)viewDidLoad
{
   [super viewDidLoad];
   
    currentlySending = false;
    
   host = @"hit4.nimbus.cip.gatech.edu";
   
   dispFormat = [[NSDateFormatter alloc] init];
   [dispFormat setDateFormat:@"MM-dd hh:mm"];
   NSUserDefaults *def = [NSUserDefaults standardUserDefaults];
   NSDate *update = [def objectForKey:@"lastUpdate"];
   _updateLabel.text = [dispFormat stringFromDate:update];
   
   if([CMMotionActivityManager isActivityAvailable])
      manager = [[CMMotionActivityManager alloc] init];
   else
      manager = nil;
   if([CMStepCounter isStepCountingAvailable])
      counter = [[CMStepCounter alloc] init];
   else
      counter = nil;
   curDay = [NSDate date];
   [self loadDataForDate:curDay];
   self.nextButton.enabled = false;
   _navBar.delegate = self;
   if ([self respondsToSelector:@selector(edgesForExtendedLayout)])
      self.edgesForExtendedLayout = UIRectEdgeNone;
}

- (void) setRandomBackgroundColor
{
    [UIView animateWithDuration:0.3f animations:^{
        CGFloat hue = ( arc4random() % 256 / 256.0 );  //  0.0 to 1.0
        UIColor *color = [UIColor colorWithHue:hue saturation:0.33f brightness:0.85f alpha:1];
        self.view.layer.backgroundColor = color.CGColor;
    }];
}

- (void) setBackgrounFromActivity:(double)act
{
    [UIView animateWithDuration:0.3f animations:^{
        double act2 = act / 60;
        CGFloat hue = ((MIN(act2, 100) / 100.0f) * 0.65f) + 0.35;
        hue = ((hue  - 0.6825f) * -1) + 0.6825f;
        UIColor *color = [UIColor colorWithHue:hue saturation:0.33f brightness:0.85f alpha:1];
        self.view.layer.backgroundColor = color.CGColor;
    }];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void) loadDataForDate:(NSDate *)date
{
    //[self setRandomBackgroundColor];
    if(manager != nil)
    {
        NSDate *from = [self begginingOfDay:date];
        
        NSDateFormatter *format = [[NSDateFormatter alloc] init];
        [format setDateFormat:@"EEEE MMM d"];
        self.dateLabel.text = [format stringFromDate:date];
        
        activityData = [NSMutableArray array];
        
        [manager queryActivityStartingFromDate:from toDate:date toQueue:[NSOperationQueue mainQueue] withHandler:^(NSArray *activities, NSError *error) {
            NSDate *prvDate = from;
            double walking = 0;
            double running = 0;
            double stationary = 0;
            double inCar = 0;
            double unknown = 0;
            bool walkBool = false;
            bool runBool = false;
            bool stationBool = true;
            bool carBool = false;
            bool unkBool = false;
            NSMutableDictionary *activityDict = [NSMutableDictionary dictionary];
            CMMotionActivity *act2;
            int actNum;
            NSDateFormatter *formatter = [[NSDateFormatter alloc] init];
            [formatter setDateFormat:@"yyyy-MM-dd HH:mm:ss.SSS"];
            for (CMMotionActivity *act in activities)
            {
                if(walkBool && prvDate != nil)
                {
                    walking += [act.startDate timeIntervalSinceDate:prvDate];
                    actNum = 1;
                }
                if(runBool && prvDate != nil)
                {
                    running += [act.startDate timeIntervalSinceDate:prvDate];
                    actNum = 2;
                }
                if(stationBool && prvDate != nil)
                {
                    stationary += [act.startDate timeIntervalSinceDate:prvDate];
                    actNum = 3;
                }
                if(carBool && prvDate != nil)
                {
                    inCar += [act.startDate timeIntervalSinceDate:prvDate];
                    actNum = 4;
                }
                if(unkBool && prvDate != nil)
                {
                    unknown += [act.startDate timeIntervalSinceDate:prvDate];
                    actNum = 5;
                }
                activityDict = [NSMutableDictionary dictionary];
                walkBool = act.walking;
                runBool = act.running;
                stationBool = act.stationary;
                carBool = act.automotive;
                
                unkBool = (!walkBool && !runBool && !stationBool && !carBool);
                
                [activityDict setValue:[NSNumber numberWithInt:actNum] forKey:@"type"];
                [activityDict setValue:[NSNumber numberWithInt:act.confidence] forKey:@"confidence"];
                [activityDict setValue:[NSNumber numberWithFloat:[act.startDate timeIntervalSinceDate:prvDate]] forKey:@"duration"];
                [activityDict setValue:[formatter stringFromDate:prvDate] forKey:@"start_time"];
                [activityDict setValue:[NSNumber numberWithInt:1] forKey:@"activityid"];
                [activityData addObject:activityDict];
                prvDate = act.startDate;
                act2 = act;
            }
            if([prvDate compare:date] == NSOrderedDescending)
            {
                if(walkBool && prvDate != nil)
                {
                    walking += [prvDate timeIntervalSinceDate:date];
                }
                if(runBool && prvDate != nil)
                {
                    running += [prvDate timeIntervalSinceDate:date];
                }
                if(stationBool && prvDate != nil)
                {
                    stationary += [prvDate timeIntervalSinceDate:date];
                }
                if(carBool && prvDate != nil)
                {
                    inCar += [prvDate timeIntervalSinceDate:date];
                }
                if(unkBool && prvDate != nil)
                {
                    unknown += [prvDate timeIntervalSinceDate:date];
                }
                activityDict = [NSMutableDictionary dictionary];
                [activityDict setValue:[NSNumber numberWithInt:actNum] forKey:@"type"];
                [activityDict setValue:[NSNumber numberWithInt:act2.confidence] forKey:@"confidence"];
                [activityDict setValue:[NSNumber numberWithFloat:[act2.startDate timeIntervalSinceDate:prvDate]] forKey:@"duration"];
                [activityDict setValue:[formatter stringFromDate:prvDate] forKey:@"start_time"];
                [activityDict setValue:[NSNumber numberWithInt:1] forKey:@"activityid"];
                [activityData addObject:activityDict];
            }
//            NSLog(@"Walking for %f seconds", walking);
//            NSLog(@"Running for %f seconds", running);
            self.walkingLabel.text = [self stringFromTimeInterval:walking];
            self.runningLabel.text = [self stringFromTimeInterval:running];
            self.carLabel.text = [self stringFromTimeInterval:inCar];
            self.stationaryLabel.text = [self stringFromTimeInterval:stationary];
            self.otherLabel.text = [self stringFromTimeInterval:unknown];
            self.totalLabel.text = [self stringFromTimeInterval:walking+running];
            double tot = walking + running + stationary + inCar + unknown;
            NSLog(@"total: %f", tot / 3600);
            [self setBackgrounFromActivity:walking+running];
            
        }];
        
        [counter queryStepCountStartingFrom:from to:date toQueue:[NSOperationQueue mainQueue] withHandler:^(NSInteger numberOfSteps, NSError *error) {
            NSLog(@"Number of steps: %ld", (long)numberOfSteps);
            self.stepLabel.text = [NSString stringWithFormat:@"%ld steps", (long)numberOfSteps];
        }];
    }
}

- (NSString *)stringFromTimeInterval:(NSTimeInterval)interval
{
    NSInteger ti = (NSInteger)interval;
    NSInteger seconds = ti % 60;
    NSInteger minutes = (ti / 60) % 60;
    NSInteger hours = (ti / 3600);
    NSString *rval;
    if(hours >= 1)
    {
        NSString *hrs = (hours > 1) ? @"hours" : @"hour";
        rval = [NSString stringWithFormat:@"%2li %@ %2li min %2li sec", (long)hours, hrs, (long)minutes, (long)seconds];
    }
    else if(minutes >= 1)
        rval = [NSString stringWithFormat:@"%2li minutes %2li sec", (long)minutes, (long)seconds];
    else
        rval = [NSString stringWithFormat:@"%2li seconds",(long)seconds];
    return rval;
}

-(NSDate *)begginingOfDay:(NSDate *)date
{
    NSCalendar *cal = [NSCalendar currentCalendar];
    NSDateComponents *components = [cal components:( NSMonthCalendarUnit | NSYearCalendarUnit | NSHourCalendarUnit | NSMinuteCalendarUnit | NSSecondCalendarUnit | NSDayCalendarUnit) fromDate:date];
    
    [components setHour:0];
    [components setMinute:0];
    [components setSecond:0];
    
    return [cal dateFromComponents:components];
    
}

-(NSDate *)endOfDay:(NSDate *)date
{
    NSCalendar *cal = [NSCalendar currentCalendar];
    NSDateComponents *components = [cal components:( NSMonthCalendarUnit | NSYearCalendarUnit | NSHourCalendarUnit | NSMinuteCalendarUnit | NSSecondCalendarUnit | NSDayCalendarUnit) fromDate:date];
    
    [components setHour:23];
    [components setMinute:59];
    [components setSecond:59];
    
    return [cal dateFromComponents:components];
}

-(NSDate *)addDay:(NSDate *)date
{
   NSCalendar *cal = [NSCalendar currentCalendar];
   NSDateComponents *components = [cal components:( NSMonthCalendarUnit | NSYearCalendarUnit | NSHourCalendarUnit | NSMinuteCalendarUnit | NSSecondCalendarUnit | NSDayCalendarUnit) fromDate:date];
   
   [components setDay:[components day]+1];
   return [cal dateFromComponents:components];
}

-(NSDate *) addDays
{
    NSDate *now = [NSDate date];
    // set up date components
    NSDateComponents *components = [[NSDateComponents alloc] init];
    [components setDay:dayOffset*-1];
    
    // create a calendar
    NSCalendar *gregorian = [[NSCalendar alloc] initWithCalendarIdentifier:NSGregorianCalendar];
    
    NSDate *rval = [gregorian dateByAddingComponents:components toDate:now options:0];
    return rval;
}

- (IBAction)previousDay:(UIButton *)sender {
    [self goPrevious];
}

- (void) goPrevious
{
    dayOffset++;
    self.nextButton.enabled = true;
    curDay = [self addDays];
    curDay = [self endOfDay:curDay];
    [self loadDataForDate:curDay];
}

- (IBAction)nextDay:(UIButton *)sender {
    [self goNext];
}

- (void) goNext
{
    dayOffset--;
    self.nextButton.enabled = dayOffset != 0;
    curDay = [self addDays];
    curDay = [self endOfDay:curDay];
    [self loadDataForDate:curDay];
}

- (IBAction)refresh:(id)sender {
    dayOffset = 0;
    self.nextButton.enabled = false;
    curDay = [NSDate date];
    [self loadDataForDate:curDay];
}

- (IBAction)rightSwipe:(UISwipeGestureRecognizer *)sender {

    [self goPrevious];
}

- (IBAction)leftSwipe:(id)sender {
    if(dayOffset > 0)
    {
        [self goNext];
    }
}

- (IBAction)sendDataPresses:(UIButton *)sender
{
    NSError *error;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:activityData options:NSJSONWritingPrettyPrinted error:&error];
    NSString *jsonStr = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
//    NSLog(@"Json data:\n%@", jsonStr);
    NSMutableURLRequest *req = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"http://hit4.nimbus.cip.gatech.edu:8080/addActivity/"]];
    [req setHTTPMethod:@"POST"];
    NSString *postBody = [NSString stringWithFormat:@"activity=%@", jsonStr];
    [req setHTTPBody:[postBody dataUsingEncoding:NSUTF8StringEncoding]];
    NSURLResponse *resp;
    NSData *respData = [NSURLConnection sendSynchronousRequest:req returningResponse:&resp error:&error];
    NSString *respStr = [[NSString alloc] initWithData:respData encoding:NSUTF8StringEncoding];
    if([respStr isEqualToString:@"true"])
    {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Success!" message:@"Data added to Database" delegate:Nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
        [alert show];
    }
    NSLog(@"Got response %@", respStr);
}

- (UIBarPosition)positionForBar:(id<UIBarPositioning>)bar
{
    return UIBarPositionTop;
}

- (void) sendData
{
    if (currentlySending) {
        return;
    }
    currentlySending = true;
   NSUserDefaults *def = [NSUserDefaults standardUserDefaults];
   NSDate *update = [def objectForKey:@"lastUpdate"];
   NSDateFormatter *formatter = [[NSDateFormatter alloc] init];
   NSDate *now = [NSDate date];
   [formatter setDateFormat:@"yyyy-MM-dd HH:mm:ss.SSS"];
   
   if(update == nil)
   {
      update = [NSDate date];
      NSCalendar *cal = [NSCalendar currentCalendar];
      NSDateComponents *components = [cal components:( NSMonthCalendarUnit | NSYearCalendarUnit | NSHourCalendarUnit | NSMinuteCalendarUnit | NSSecondCalendarUnit | NSDayCalendarUnit) fromDate:update];
      
      [components setHour:0];
      [components setMinute:0];
      [components setSecond:0];
      [components setDay:[components day] - 7];
      
      update = [cal dateFromComponents:components];
      
   }
   NSDate *end = [self endOfDay:update];
   activityData = [NSMutableArray array];
   NSOperation *opp = [[NSOperation alloc] init];
   NSOperationQueue* aQueue = [[NSOperationQueue alloc] init];
   [manager queryActivityStartingFromDate:update toDate:now toQueue:aQueue withHandler:^(NSArray *activities, NSError *error) {
      NSDate *prvDate = [update copy];
      double walking = 0;
      double running = 0;
      double stationary = 0;
      double inCar = 0;
      double unknown = 0;
      bool walkBool = false;
      bool runBool = false;
      bool stationBool = true;
      bool carBool = false;
      bool unkBool = false;
      NSMutableDictionary *activityDict = [NSMutableDictionary dictionary];
      CMMotionActivity *act2;
      int actNum;
      NSMutableArray *actArr = [NSMutableArray array];
      for (CMMotionActivity *act in activities)
      {
         if(walkBool && prvDate != nil)
         {
            walking += [act.startDate timeIntervalSinceDate:prvDate];
            actNum = 1;
         }
         if(runBool && prvDate != nil)
         {
            running += [act.startDate timeIntervalSinceDate:prvDate];
            actNum = 2;
         }
         if(stationBool && prvDate != nil)
         {
            stationary += [act.startDate timeIntervalSinceDate:prvDate];
            actNum = 3;
         }
         if(carBool && prvDate != nil)
         {
            inCar += [act.startDate timeIntervalSinceDate:prvDate];
            actNum = 4;
         }
         if(unkBool && prvDate != nil)
         {
            unknown += [act.startDate timeIntervalSinceDate:prvDate];
            actNum = 5;
         }
         activityDict = [NSMutableDictionary dictionary];
         walkBool = act.walking;
         runBool = act.running;
         stationBool = act.stationary;
         carBool = act.automotive;
         
         unkBool = (!walkBool && !runBool && !stationBool && !carBool);
         
         [activityDict setValue:[NSNumber numberWithInt:actNum] forKey:@"type"];
         [activityDict setValue:[NSNumber numberWithInt:act.confidence] forKey:@"confidence"];
         [activityDict setValue:[NSNumber numberWithFloat:[act.startDate timeIntervalSinceDate:prvDate]] forKey:@"duration"];
         [activityDict setValue:[formatter stringFromDate:prvDate] forKey:@"start_time"];
         [activityDict setValue:[NSNumber numberWithInt:1] forKey:@"activityid"];
         [actArr addObject:activityDict];
         prvDate = act.startDate;
         act2 = act;
      }
      if([prvDate compare:update] == NSOrderedDescending)
      {
         if(walkBool && prvDate != nil)
         {
            walking += [prvDate timeIntervalSinceDate:update];
         }
         if(runBool && prvDate != nil)
         {
            running += [prvDate timeIntervalSinceDate:update];
         }
         if(stationBool && prvDate != nil)
         {
            stationary += [prvDate timeIntervalSinceDate:update];
         }
         if(carBool && prvDate != nil)
         {
            inCar += [prvDate timeIntervalSinceDate:update];
         }
         if(unkBool && prvDate != nil)
         {
            unknown += [prvDate timeIntervalSinceDate:update];
         }
         activityDict = [NSMutableDictionary dictionary];
         [activityDict setValue:[NSNumber numberWithInt:actNum] forKey:@"type"];
         [activityDict setValue:[NSNumber numberWithInt:act2.confidence] forKey:@"confidence"];
         [activityDict setValue:[NSNumber numberWithFloat:[act2.startDate timeIntervalSinceDate:prvDate]] forKey:@"duration"];
         [activityDict setValue:[formatter stringFromDate:prvDate] forKey:@"start_time"];
         [activityDict setValue:[NSNumber numberWithInt:1] forKey:@"activityid"];
         [actArr addObject:activityDict];
      }
      NSData *jsonData = [NSJSONSerialization dataWithJSONObject:actArr options:NSJSONWritingPrettyPrinted error:&error];
      __block NSString *jsonStr = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
      dispatch_sync(dispatch_get_main_queue(), ^{
      //    NSLog(@"Json data:\n%@", jsonStr);
         NSString *url = [NSString stringWithFormat:@"https://%@/addActivity/", host];
         NSLog(@"Sending activity to %@", url);
         NSMutableURLRequest *req = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:url]];
         [req setTimeoutInterval:100000];
         [req setHTTPMethod:@"POST"];
         NSString *postBody = [NSString stringWithFormat:@"activity=%@", jsonStr];
         [req setHTTPBody:[postBody dataUsingEncoding:NSUTF8StringEncoding]];
         NSLog(@"Sending %lu activites", (unsigned long)[actArr count]);
         sendActCon = [NSURLConnection connectionWithRequest:req delegate:self];
      });
      actArr = nil;
   }];
   
   stepData = [NSMutableArray array];
   
   update = [self begginingOfDay:update];
   end = [self endOfDay:update];
   
   //step through the days to send step data... no pun intended!
   dispatch_semaphore_t sema = dispatch_semaphore_create(0);
   do
   {
      __block NSDictionary *stepDict = [NSMutableDictionary dictionary];
      [counter queryStepCountStartingFrom:update to:end toQueue:[NSOperationQueue mainQueue] withHandler:^(NSInteger numberOfSteps, NSError *error) {
         NSLog(@"Number of steps: %ld", (long)numberOfSteps);
         [stepDict setValue:[NSNumber numberWithInt:1] forKey:@"stepid"];
         [stepDict setValue:[NSNumber numberWithLong:numberOfSteps] forKey:@"number_steps"];
         [stepDict setValue:[formatter stringFromDate:end] forKey:@"date"];
         
         dispatch_semaphore_signal(sema);
      }];
      
      dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER);
      [stepData addObject:stepDict];
      
      update = [self begginingOfDay:update];
      update = [self addDay:update];
      end = [now compare:[self addDay:end]] == NSOrderedDescending ? [self addDay:end] : now;
   } while ([update compare:[NSDate date]] == NSOrderedAscending);
   NSError *error;
   NSData *jsonData = [NSJSONSerialization dataWithJSONObject:stepData options:NSJSONWritingPrettyPrinted error:&error];
   
   __block NSString *jsonStr = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
   dispatch_sync(dispatch_get_main_queue(), ^{
//   NSLog(@"Json data:\n%@", jsonStr);
      NSMutableURLRequest *req = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:[NSString stringWithFormat:@"https://%@/addSteps/", host]]];
      [req setHTTPMethod:@"POST"];
      NSString *postBody = [NSString stringWithFormat:@"steps=%@", jsonStr];
      [req setHTTPBody:[postBody dataUsingEncoding:NSUTF8StringEncoding]];
      sendStepsCon = [NSURLConnection connectionWithRequest:req delegate:self];
   });
   
}

- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
   NSString *recStr = [NSString stringWithUTF8String:[data bytes]];
   NSLog(@"Got data - %@", recStr);
   if(connection == sendActCon)
   {
      NSUserDefaults *def = [NSUserDefaults standardUserDefaults];
      if([recStr isEqualToString:@"true"])
      {
         NSLog(@"Activity posted!");
         NSDate *meow = [NSDate date];
         [def setObject:meow forKey:@"lastUpdate"];
         _updateLabel.text = [dispFormat stringFromDate:meow];
         
         [self scheduleNotification];
      } else
      {
         NSLog(@"Error with Activity! - %@", recStr);
      }
       currentlySending = false;

   } else if(connection == sendStepsCon)
   {
      if([recStr isEqualToString:@"True"])
      {
         NSLog(@"added steps!");
      } else
      {
         NSLog(@"Error with steps! - %@", recStr);
      }
   }
}

-(void) scheduleNotification
{
   [UIApplication sharedApplication].applicationIconBadgeNumber = 0;
   [[UIApplication sharedApplication] cancelAllLocalNotifications];
   UILocalNotification *localNotif = [[UILocalNotification alloc] init];
   localNotif.timeZone = [NSTimeZone defaultTimeZone];
   NSDate *now = [NSDate date];
   NSDate *future1 = [now dateByAddingTimeInterval:(60 * 60 * 24) * 1];
   localNotif.fireDate = future1;
   localNotif.alertBody = @"Please open the Activity app to send data 😃";
   localNotif.alertAction = @"Open";
   localNotif.soundName = UILocalNotificationDefaultSoundName;
   localNotif.applicationIconBadgeNumber = 1;
   [[UIApplication sharedApplication] scheduleLocalNotification:localNotif];
   
   UILocalNotification *localNotif2 = [[UILocalNotification alloc] init];
   localNotif2.timeZone = [NSTimeZone defaultTimeZone];
   localNotif2.fireDate = [now dateByAddingTimeInterval:(60 * 60 * 24) * 3];
   localNotif2.alertBody = @"Please open the Activity app to send data 😃";
   localNotif2.alertAction = @"Open";
   localNotif2.soundName = UILocalNotificationDefaultSoundName;
   localNotif2.applicationIconBadgeNumber = 2;
   [[UIApplication sharedApplication] scheduleLocalNotification:localNotif2];
   
   UILocalNotification *localNotif3 = [[UILocalNotification alloc] init];
   localNotif3.timeZone = [NSTimeZone defaultTimeZone];
   localNotif3.fireDate = [now dateByAddingTimeInterval:(60 * 60 * 24) * 4];
   localNotif3.alertBody = @"Please open the Activity app to send data 😃";
   localNotif3.alertAction = @"Open";
   localNotif3.soundName = UILocalNotificationDefaultSoundName;
   localNotif3.applicationIconBadgeNumber = 3;
   [[UIApplication sharedApplication] scheduleLocalNotification:localNotif3];
   
   UILocalNotification *localNotif4 = [[UILocalNotification alloc] init];
   localNotif4.timeZone = [NSTimeZone defaultTimeZone];
   localNotif4.fireDate = [now dateByAddingTimeInterval:(60 * 60 * 24) * 5];
   localNotif4.alertBody = @"Please open the Activity app to send data 😃";
   localNotif4.alertAction = @"Open";
   localNotif4.soundName = UILocalNotificationDefaultSoundName;
   localNotif4.applicationIconBadgeNumber = 4;
   [[UIApplication sharedApplication] scheduleLocalNotification:localNotif4];
}

- (BOOL)connection:(NSURLConnection *)connection canAuthenticateAgainstProtectionSpace:(NSURLProtectionSpace *)protectionSpace
{
   NSLog(@"canAuthenticateAgainstProtectionSpace -> %@", protectionSpace.authenticationMethod);
   return [protectionSpace.authenticationMethod isEqualToString:NSURLAuthenticationMethodServerTrust] || [protectionSpace.authenticationMethod isEqualToString:NSURLAuthenticationMethodHTTPBasic];
   //return true;
}

- (void)connection:(NSURLConnection *)connection didReceiveAuthenticationChallenge:(NSURLAuthenticationChallenge *)challenge
{
   NSLog(@"auth challenge");
   if(connection == sendActCon || connection == sendStepsCon)
   {
      NSArray *trustedHosts = [[NSArray alloc] initWithObjects:host, nil];
      if ([challenge.protectionSpace.authenticationMethod isEqualToString:NSURLAuthenticationMethodServerTrust])
      {
         NSLog(@"server trust -> %@", challenge.protectionSpace.host);
         if ([trustedHosts containsObject:challenge.protectionSpace.host])
         {
            [challenge.sender useCredential:[NSURLCredential credentialForTrust:challenge.protectionSpace.serverTrust] forAuthenticationChallenge:challenge];
            //            NSURLCredential* credential = [[NSURLCredential alloc] initWithUser:@"admin" password:@"" persistence:NSURLCredentialPersistenceForSession];
            //            [[challenge sender] useCredential:credential forAuthenticationChallenge:challenge];
            
         }
         [challenge.sender continueWithoutCredentialForAuthenticationChallenge:challenge];
      }
      
   }
   
}

- (void)connection:(NSURLConnection *)connection didFailWithError:(NSError *)error
{
   NSLog(@"Error :( - %@", error);
}

@end
