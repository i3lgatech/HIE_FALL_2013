//
//  ViewController.h
//  ActivityMonitor
//
//  Created by Rob Stevenson on 9/30/13.
//  Copyright (c) 2013 Rob Stevenson. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ViewController : UIViewController<UIBarPositioningDelegate, NSURLConnectionDelegate>

- (IBAction)previousDay:(UIButton *)sender;
- (IBAction)nextDay:(UIButton *)sender;
- (IBAction)refresh:(id)sender;
- (IBAction)rightSwipe:(UISwipeGestureRecognizer *)sender;
- (IBAction)leftSwipe:(id)sender;
- (IBAction)sendDataPresses:(UIButton *)sender;

- (void) sendData;

@property (strong, nonatomic) IBOutlet UILabel *walkingLabel;
@property (strong, nonatomic) IBOutlet UILabel *runningLabel;
@property (strong, nonatomic) IBOutlet UILabel *stationaryLabel;
@property (strong, nonatomic) IBOutlet UILabel *carLabel;
@property (strong, nonatomic) IBOutlet UILabel *stepLabel;
@property (strong, nonatomic) IBOutlet UILabel *totalLabel;
@property (strong, nonatomic) IBOutlet UILabel *dateLabel;
@property (strong, nonatomic) IBOutlet UILabel *otherLabel;
@property (strong, nonatomic) IBOutlet UIButton *nextButton;
@property (strong, nonatomic) IBOutlet UINavigationBar *navBar;
@property (strong, nonatomic) IBOutlet UILabel *updateLabel;
@end
