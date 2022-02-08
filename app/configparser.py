import json
from .models import Class, Subject, Bucket, SBucket, STest, SGrade
from . import db
from flask_login import current_user

def parse(config_json):
    config = json.loads(config_json)

      ## Test required options
    if not "name" in config.keys() or not "min_presence" in config.keys() or not "weeks" in config.keys() or not "subject_buckets" in config.keys():
        return "NOK_REQ"

    print("Config detected for " + config["name"])

    class_name = config["name"]
    if not Class.query.filter_by(class_name=class_name).first():
        print("No existing class found for " + class_name)
        return "NOK_NEX"
    class_obj = Class.query.filter_by(id=current_user.class_id).first()
    class_id = class_obj.id
    class_min_presence = config["min_presence"]
    if "%" in class_min_presence:
        class_min_presence = int(class_min_presence.replace("%", ""))

    if not class_min_presence > 0 or not class_min_presence < 100:
        return "NOK_PTL"

    print("Minimum presence of " + str(class_min_presence) + '% detected')

    weeks = int(config["weeks"])
    if not weeks > 10 or not weeks < 50:
        return "NOK_WCT"

    print("The class will be set up for " + str(weeks) + " weeks")

    class_obj.min_presence = class_min_presence
    class_obj.weeks = weeks

      ## Analyze main grade buckets
    subject_buckets = config["subject_buckets"]
    for subject in subject_buckets:

        ## Test important keys
        if not "name" in subject.keys() or not "single" in subject.keys():
            return "NOK_SJK"
        
        s_name = subject["name"]
        s_single = True

        if subject["single"] == "no" or subject["single"] == "No" or subject["single"] == "false" or subject["single"] == "False":
            s_single = False

        if s_single == True:
            s_weekly = int(subject["weekly"])
            if "finals" in subject.keys():
                s_finals = int(subject["finals"].replace("%", ""))
            else:
                s_finals = 0
            print("Subject: " + s_name + " takes place " + str(s_weekly) + " times per week with finals counting " + str(s_finals) + "%.")
            subject = Subject(name=s_name, weekly=s_weekly, finals=s_finals, class_id=class_id)
            db.session.add(subject)
            db.session.commit()

        if s_single == False:
            tertiary = False
            primary_finals = 0
            primary_weekly = 0
            primary_weight = 0
            primary_name = ""

            secondary_finals = 0
            secondary_weekly = 0
            secondary_weight = 0
            secondary_name = ""

            tertiary_finals = 0
            tertiary_weekly = 0
            tertiary_weight = 0
            tertiary_name = 0

            if "1" in subject.keys():
                if not "1_counts" in subject.keys():
                    return "NOK_SJK"
                if not "1_weekly" in subject.keys():
                    return "NOK_SJK"
                primary_finals = 0
                if "1_finals" in subject.keys():
                    primary_finals = int(subject["1_finals"].replace("%", ""))
                primary_name = subject["1"]
                primary_weekly = int(subject["1_weekly"])
                primary_weight = int(subject["1_counts"].replace("%", ""))
            
            if "2" in subject.keys():
                if not "2_counts" in subject.keys():
                    secondary_weight = 100 - primary_weight
                else:
                    secondary_weight = int(subject["2_counts"].replace("%", ""))
                if not "2_weekly" in subject.keys():
                    return "NOK_SJK"
                secondary_finals = 0
                if "2_finals" in subject.keys():
                    secondary_finals = int(subject["2_finals"].replace("%", ""))
                secondary_name = subject["2"]
                secondary_weekly = int(subject["2_weekly"])
                secondary_weight = int(subject["2_counts"].replace("%", ""))

            if "3" in subject.keys():
                if not "3_counts" in subject.keys():
                    tertiary_weight = 100 - primary_weight - secondary_weight
                else:
                    tertiary_weight = int(subject["3_counts"].replace("%", ""))
                if not "3_weekly" in subject.keys():
                    return "NOK_SJK"
                tertiary_finals = 0
                if "3_finals" in subject.keys():
                    tertiary_finals = int(subject["3_finals"].replace("%", ""))
                tertiary = True
                tertiary_name = subject["3"]
                tertiary_weekly = int(subject["3_weekly"])

            if tertiary == True:
                print("Found and processed subject bucket consisting of " + primary_name + ", " + secondary_name + " and " + tertiary_name + ".")
            else:
                print("Found and processed subject bucket consisting of " + primary_name + " and " + secondary_name + ".")

            bucket = Bucket(name=s_name, class_id=class_id)
            db.session.add(bucket)
            db.session.commit()

            bucket_id = Bucket.query.filter_by(name=s_name, class_id=class_id).first().id
            
            primary_subject = Subject(name=primary_name, class_id=class_id, bucket_id=bucket_id, bucket_bool=True, weight=primary_weight, finals=primary_finals, weekly=primary_weekly)
            secondary_subject = Subject(name=secondary_name, class_id=class_id, bucket_id=bucket_id, bucket_bool=True, weight=secondary_weight, finals=secondary_finals, weekly=secondary_weekly)
            db.session.add(primary_subject)
            db.session.add(secondary_subject)
            if tertiary:
                tertiary_subject = Subject(name=tertiary_name, class_id=class_id, bucket_id=bucket_id, bucket_bool=True, weight=tertiary_weight, finals=tertiary_finals, weekly=tertiary_weekly)
                db.session.add(tertiary_subject)
            db.session.commit()

    ssubject_buckets = config["special_subjects"]
    for subject in ssubject_buckets:
        name = subject["name"]
        num = subject["grades"]
        presence = True if subject["presence"] == "yes" or "Yes" or "True" or "true" else False
        weekly = subject["weekly"]

        test_ids = []
        iter = 1
        while iter <= num:
            weight = int(subject[str(iter) + "_counts"].replace("%", ""))
            name = str(iter)
            if str(iter) + "_name" in subject.keys():
                name = subject[str(iter) + "_name"]
            stest = STest(name=name, class_id=class_id, weight=weight)
            db.session.add(stest)
            db.session.commit()

            stest_id = STest.query.filter_by(name=name, class_id=class_id).first().id
            test_ids.append(stest_id)
            iter += 1
        
        sbucket = SBucket(name=subject["name"], tests=test_ids, class_id=class_id)
        db.session.add(sbucket)
        db.session.commit()