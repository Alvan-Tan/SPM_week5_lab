import unittest
import flask_testing
import json
from app import app, db, Course, Academic_record, Enrollment


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.c1 = Course(CID='IS500', name='Super Mod', prerequisites='', trainers='')
        self.c2 = Course(CID='IS600', name='Super Hard Mod', prerequisites='IS500', trainers='')
        self.er1 = Enrollment(EID=1, SID='G2', CID='IS500')
        self.er2 = Enrollment(EID=6, SID='G90', CID='IS600')
        self.cd1 = Academic_record(EID=1, SID="G2", CID="IS500", QID=1, status='ongoing', quiz_result=0)
        self.cd2 = Academic_record(EID=2, SID="G12", CID="IS600", QID=1, status='ongoing', quiz_result=0)
        
        db.create_all()


    def tearDown(self):
        # self.e1 = None
        self.c1 = None
        self.c2 = None
        self.er1 = None
        self.er2 = None
        self.cd1 = None
        self.cd2 = None
        db.session.remove()
        db.drop_all()


### Registration TEST CASES ###
class TestEngineerSignup(TestApp):
    # Testing positive case where all details are present in request body
    def test_engineer_signup_all_details(self):
        # creating request body for signup details
        request_body = {
            'EID': self.er1.EID,
            'SID': self.er1.SID,
            'CID': self.er1.CID
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                {
                'EID': 1,
                'SID': 'G2',
                'CID': 'IS500',
                }
                ,
            'message' : f'{self.er1.EID} engineer has been updated successfully in the database'
            }) 


    # Testing negative case where EID is missing in request body
    def test_engineer_signup_eid_missing(self):
        # creating request body for signup details
        request_body = {
            'SID': self.er1.SID,
            'CID': self.er1.CID,
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Enrollment ['EID'] is not present,  engineer is not enrolled"
            })


    # Testing negative case where SID is missing in request body
    def test_engineer_signup_sid_missing(self):
        # creating request body for signup details
        request_body = {
            'EID': self.er1.EID,
            'CID': self.er1.CID
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Enrollment ['SID'] is not present,  engineer is not enrolled"
            })


    # Testing negative case where CID is missing in request body
    def test_engineer_signup_cid_missing(self):
        # creating request body for signup details
        request_body = {
            'EID': self.er1.EID,
            'SID': self.er1.SID
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Enrollment ['CID'] is not present,  engineer is not enrolled"
            })
    

class TestHRViewSignup(TestApp):
    # Testing function when database has no signups
    def test_hr_view_signup_0(self):
        # calling hr_view_signup function via flask route
        response = self.client.get("/hr_view_signup")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : 'There are no enrollment retrieved'
        })


    # Testing function when database has 1 signups
    def test_hr_view_signup_1(self):
        # adding dummy signups to database
        db.session.add(self.er1)
        db.session.commit()
        
        # calling hr_view_signup function via flask route
        response = self.client.get("/hr_view_signup")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                [
                {
                'EID': 1,
                'SID': 'G2',
                'CID': 'IS500',
                }
                ]
                ,
            'message' : 'All enrollments are retrieved'
            })


    # Testing function when database has 2 signups
    def test_hr_view_signup_2(self):
        # adding dummy signups to database
        db.session.add(self.er1)
        db.session.add(self.er2)
        db.session.commit()
        
        # calling hr_view_signup function via flask route
        response = self.client.get("/hr_view_signup")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                [
                {
                'EID': 1,
                'SID': 'G2',
                'CID': 'IS500',
                },
                {
                'EID': 6,
                'SID': 'G90',
                'CID': 'IS600',
                },
                ]
                ,
            'message' : 'All enrollments are retrieved'
            })


class TestHRAssignEngineer(TestApp):
    # Testing positive case where all details are present in request body
    def test_hr_assign_engineer_all_details(self):
        # creating request body for assignment details
        request_body = {
            'EID': self.cd1.EID,
            'SID': self.cd1.SID,
            'CID': self.cd1.CID,
            'QID': self.cd1.QID,
            'status': self.cd1.status,
            'quiz_result': self.cd1.quiz_result
        }

        # calling hr_assign_engineer function via flask route
        response = self.client.post("/hr_assign_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                {
                'EID': 1,
                'SID': 'G2',
                'CID': 'IS500',
                'QID': 1,
                'status': 'ongoing',
                'quiz_result': 0
                },
            'message' : f'{self.cd1.EID} has been inserted successfully into the course details'
            })


    # Testing negative case where EID missing in request body
    def test_hr_assign_engineer_missing_eid(self):
        # creating request body for assignment details
        request_body = {
            'SID': self.cd1.SID,
            'CID': self.cd1.CID,
            'QID': self.cd1.QID,
            'status': self.cd1.status,
            'quiz_result': self.cd1.quiz_result
        }

        # calling hr_assign_engineer function via flask route
        response = self.client.post("/hr_assign_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"academic record ['EID'] is not present,  engineer is not assigned"
            })


class TestHRWithdrawEngineer(TestApp):
    # Testing positive case where course detail is in database
    def test_hr_withdraw_engineer_in_database(self):
        # adding dummy course detail into database
        db.session.add(self.cd2)
        db.session.commit()

        # creating request body for withdraw details
        request_body = {
            'EID': self.cd2.EID,
            'SID': self.cd2.SID,
            'CID': self.cd2.CID,
            'QID': self.cd2.QID,
            'status': self.cd2.status,
            'quiz_result': self.cd2.quiz_result
        }

        # calling hr_withdraw_engineer function via flask route
        response = self.client.post("/hr_withdraw_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f'{self.cd2.EID} has been deleted successfully from course details'
            })
    

    # Testing negative case where course detail is not in database
    # def test_hr_withdraw_engineer_not_in_database(self):
    #     # creating request body for withdraw details
    #     request_body = {
    #         'EID': self.cd2.EID,
    #         'SID': self.cd2.SID,
    #         'CID': self.cd2.CID,
    #         'QID': self.cd2.QID,
    #         'status': self.cd2.status,
    #         'quiz_result': self.cd2.quiz_result
    #     }

    #     # calling hr_withdraw_engineer function via flask route
    #     response = self.client.post("/hr_withdraw_engineer",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
        
    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(response.json, {
    #         'message' : f'{self.cd2.EID} is not deleted'
    #         })


    # Testing negative case where EID missing
    def test_hr_withdraw_engineer_missing_eid(self):
        # creating request body for withdraw details
        request_body = {
            'SID': self.cd2.SID,
            'CID': self.cd2.CID,
            'QID': self.cd2.QID,
            'status': self.cd2.status,
            'quiz_result': self.cd2.quiz_result
        }

        # calling hr_withdraw_engineer function via flask route
        response = self.client.post("/hr_withdraw_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"academic_record ['EID'] is not present,  engineer is not withdrawn"
            })


    # Testing negative case where CID missing
    def test_hr_withdraw_engineer_missing_cid(self):
        # creating request body for withdraw details
        request_body = {
            'EID': self.cd2.EID,
            'SID': self.cd2.SID,
            'QID': self.cd2.QID,
            'status': self.cd2.status,
            'quiz_result': self.cd2.quiz_result
        }

        # calling hr_withdraw_engineer function via flask route
        response = self.client.post("/hr_withdraw_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"academic_record ['CID'] is not present,  engineer is not withdrawn"
            })


class TestHRApproveSignup(TestApp):
    # Testing positive case where enrollment detail is in database
    def test_hr_approve_signup_in_database(self):
        # adding dummy enrollment into database
        db.session.add(self.er1)
        db.session.commit()

        # creating request body for course details
        request_body = {
            'EID': self.cd1.EID,
            'SID': self.cd1.SID,
            'CID': self.cd1.CID,
            'QID': self.cd1.QID,
            'status': self.cd1.status,
            'quiz_result': self.cd1.quiz_result
        }

        # calling hr_approve_signup function via flask route
        response = self.client.post("/hr_approve_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'EID': 1,
                'SID': 'G2',
                'CID': 'IS500',
                'QID': 1,
                'status': 'ongoing',
                'quiz_result': 0
                },
            'message' : f'{self.cd1.EID} prerequisites has been moved successfully from Enrollment to academic_record'
            })
    

    # Testing negative case where enrollment detail is not in database
    # def test_hr_approve_signup_not_in_database(self):
    #     # creating request body for course details
    #     request_body = {
    #         'EID': self.cd1.EID,
    #         'SID': self.cd1.SID,
    #         'CID': self.cd1.CID,
    #         'QID': self.cd1.QID,
    #         'status': self.cd1.status,
    #         'quiz_result': self.cd1.quiz_result
    #     }

    #     # calling hr_approve_signup function via flask route
    #     response = self.client.post("/hr_approve_signup",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(response.json, {
    #         'message' : f'{self.cd1.EID} prerequisites is not moved successfully'
    #         })


    # Testing negative case where EID is missing 
    def test_hr_approve_signup_missing_eid(self):
        # adding dummy enrollment into database
        db.session.add(self.er1)
        db.session.commit

        # creating request body for course details
        request_body = {
            'SID': self.cd1.SID,
            'CID': self.cd1.CID,
            'QID': self.cd1.QID,
            'status': self.cd1.status,
            'quiz_result': self.cd1.quiz_result
        }

        # calling hr_approve_signup function via flask route
        response = self.client.post("/hr_approve_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Academic record ['EID'] is not present,  engineer is not enrolled"
            })


    
class TestHRRejectSignup(TestApp):
    # Testing positive case where enrollment detail is in database
    def test_hr_reject_signup_in_database(self):
        # adding dummy enrollment into database
        db.session.add(self.er2)
        db.session.commit()

        # creating request body for course details
        request_body = {
            'EID': self.er2.EID,
            'SID': self.er2.SID,
            'CID': self.er2.CID,
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/hr_reject_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {

            'message' : f'{self.er2.EID} has been deleted successfully from Enrollment'
            
            })


    # Testing negative case where enrollment detail is not in database
    # def test_hr_reject_signup_not_in_database(self):

    #     # creating request body for course details
    #     request_body = {
    #         'EID': self.er2.EID,
    #         'SID': self.er2.SID,
    #         'CID': self.er2.CID,
    #     }

    #     # calling hr_reject_signup function via flask route
    #     response = self.client.post("/hr_reject_signup",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(response.json, {

    #         'message' : f'{self.er2.EID} is not deleted'
            
    #         })


    # Testing negative case where EID is missing
    def test_hr_reject_signup_missing_eid(self):
        # adding dummy enrollment into database
        db.session.add(self.er2)
        db.session.commit()

        # creating request body for course details
        request_body = {
   
            'SID': self.er2.SID,
            'CID': self.er2.CID,
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/hr_reject_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {

            'message' : f"Academic record ['EID'] is not present, signup is not rejected"
            
            })


class TestHRAssignTrainer(TestApp):
    def test_hr_assign_trainer(self):
        # adding dummy course into database
        db.session.add(self.c2)
        db.session.commit()

        # creating request body for course 
        request_body = {
            'CID' : self.c2.CID, 
            'name' : self.c2.name, 
            'prerequisites' : self.c2.prerequisites, 
            'TID' : '12,14'
        }

        # calling hr_assign_trainer function via flask route
        response = self.client.post("/hr_assign_trainer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'CID': 'IS600',
                'name' : 'Super Hard Mod',
                'prerequisites': 'IS500',
                'trainers': '12,14'
                },
            'message' : f'Trainers 12,14 has been updated successfully in the database'
            
            })


### Registration TEST CASES ###

if __name__ == '__main__':
    unittest.main()
