//
//  Activity.h
//  ActivityMonitor
//
//  Created by Rob Stevenson on 11/3/13.
//  Copyright (c) 2013 Rob Stevenson. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface Activity : NSObject

@property (nonatomic, strong) NSNumber *type;
@property (nonatomic, strong) NSNumber *duration;
@property (nonatomic, strong) NSDate *start;
@property (nonatomic, strong) NSNumber *confidence;


@end
