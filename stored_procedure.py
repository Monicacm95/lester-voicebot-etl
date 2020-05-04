import pymssql
import json

def next_question(Question_id,Option):
    Q_id = Question_id
    O_id = Option
    print(Q_id,O_id)
    
    try:
        connection = pymssql.connect(server="104.198.75.59", user='sqlserver', password='mssql@lester', database='gie151cb')
        print("connected")
        cursor = connection.cursor(as_dict=True)
        print("got cursor")
        cursor.execute('''select distinct Q_ScreenNo,DemoTypeCode,O_Type,(case CLogic when '' then 'N' else CLogic end) Q_CLogic,Next_Q 
	       FROM gie151cb.dbo.Q_Master WHERE Q_ID= {}'''.format(Q_id))
         
        profiles = cursor.fetchall()
        print(profiles)
        for d in profiles:
            if any(d['DemoTypeCode'] in (1,2) for d in profiles):
                print("DemoTypeCode",d['DemoTypeCode'])
                if any(d['O_Type'] =='O' for d in profiles):
                    print(d['O_Type']) 
                    if O_id is not None:
                        cursor.execute("""SELECT COUNT(*) i_count FROM gie151cb.dbo.Q_Options q INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={} AND q.O_String='{}'""".format(Q_id,O_id))
                        count = cursor.fetchone()
                        print("Q_ID and Option as input record count = ",count)
                        if (count["i_count"]) == 0:
                            cursor.execute("""SELECT COUNT(*) i_count FROM gie151cb.dbo.Q_Options q INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={}""".format(Q_id))   
                            count = cursor.fetchone()
                            print("count" , count)
                            if (count["i_count"]) > 1:
                                cursor.execute("""SELECT CtrlEnabled FROM gie151cb.dbo.Q_Options q WHERE q.Q_ID={} AND q.CtrlEnabled<>'N'""".format(Q_id)) 
                                CtrlEnabled = cursor.fetchall()
                                if CtrlEnabled:
                                    if(CtrlEnabled[0]['CtrlEnabled'] == 'T'):
                                        cursor.execute("""SELECT q.CtrlEnabled,q.ReturnValue,r.ColumnName,r.ColumnSize FROM gie151cb.dbo.Q_Options q 
INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={} AND r.ColumnName LIKE '%OTH'""".format(Q_id))
                                        Q_Options = cursor.fetchall()
                                    elif(CtrlEnabled[0]['CtrlEnabled'] == 'B'):
                                        cursor.execute("""SELECT q.CtrlEnabled,q.ReturnValue,r.ColumnName,r.ColumnSize FROM gie151cb.dbo.Q_Options q 
INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={} AND q.CtrlEnabled='B'""".format(Q_id))
                                        Q_Options = cursor.fetchall()
                                    else:
                                        cursor.execute("""SELECT q.CtrlEnabled,q.ReturnValue,r.ColumnName,r.ColumnSize FROM gie151cb.dbo.Q_Options q 
INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={} AND q.CtrlEnabled='CtrlEnabled[0]["CtrlEnabled"]'""".format(Q_id))
                                        Q_Options = cursor.fetchall()
                                        print(Q_Options)
                            else:
                                cursor.execute("""SELECT q.CtrlEnabled,q.ReturnValue,r.ColumnName,r.ColumnSize FROM gie151cb.dbo.Q_Options q 
INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={} AND  q.O_String='{}'""".format(Q_id,O_id))
                                Q_Options = cursor.fetchall()     
                                print(Q_Options)
                        else:
                            #*Change for showing only Subscriber part of the question*/
                            cursor.execute("""SELECT Q_String,Q_ID FROM gie151cb.dbo.Q_Master WHERE Q_ID={}""".format(Q_id))
                            Q_Master = cursor.fetchall()
                            Q_String1 =  Q_Master[0]["Q_String"]
                            Q_String2 = Q_String1.replace("<AgentName>", "John")
                            if (Q_String2.find("<|>")) > 0 :
                                Q_String = Q_String2.partition('<|>')[0]
                                print(Q_String)
                            if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                 print("Found {}")
                                 Status = "True"
                                 while (Status == 'True'):
                                     i_Start = Q_String.find("{")
                                     i_End = Q_String.find('}',Q_String.find("{"))
                                     slice_object = slice(i_Start+1,i_End)
                                     Q_Temp1 = Q_String[slice_object]
                                     cursor.execute("""SELECT Q_Temp2=COALESCE('{}','''') FROM gie151cb.dbo.Orglead WHERE UNID='407500192391'""".format(Q_Temp1))
                                     Q_temp2 = cursor.fetchone()
                                     print(Q_temp2["Q_Temp2"])
                                     Q_String = Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                     if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                        Status = "True"
                                     else:
                                        Status = "False"
                                 Q_String= Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                 Q_String = Q_String.replace("{" , "")
                                 Q_String = Q_String.replace("}" , "")
                                 print(Q_String)
                            else:
                                 Q_String = Q_String2.partition('<|>')[0]
                            print(Q_id, Q_String)
                                   
                            cursor.execute("""SELECT q.O_String, CtrlEnabled FROM gie151cb.dbo.Q_Options q INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={}""".format(Q_id))
                            Response =cursor.fetchall()
                            print(Response)
                elif any(d['O_Type'] =='M' for d in profiles):
                    print(d['O_Type'])
                    if O_id is not None:
                        cursor.execute("""SELECT q.CtrlEnabled,q.ReturnValue,r.ColumnName,r.ColumnSize FROM gie151cb.dbo.Q_Options q 
INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE q.Q_ID={} AND AND q.O_String='{}'""".format(Q_id,O_id))
                        Q_Options = cursor.fetchall() 
                        print(Q_Options)
   #SELECT m.Q_String, m.Q_ID FROM gie151cb.Q_Master m WHERE Q_ID=@qidnumber,
   # Change for showing only Subscriber part of the question
                    else:
                        cursor.execute("""SELECT Q_String,Q_ID FROM gie151cb.dbo.Q_Master WHERE Q_ID={}""".format(Q_id))
                        Q_Master = cursor.fetchall()
                        Q_String1 =  Q_Master["Q_String"]
                        Q_String2 = Q_String1.replace("<AgentName>", "John")
                        if (Q_String2.find("<|>")) > 0 :
                            Q_String = Q_String2.partition('<|>')[0]
                            print(Q_String)
                        if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                            print("Found {}")
                            Status = "True"
                            while (Status == 'True'):
                                 i_Start = Q_String.find("{")
                                 i_End = Q_String.find('}',Q_String.find("{"))
                                 slice_object = slice(i_Start+1,i_End)
                                 Q_Temp1 = Q_String[slice_object]
                                 cursor.execute("""SELECT Q_Temp2=COALESCE('{}','''') FROM gie151cb.dbo.Orglead WHERE UNID='407500192391'""".format(Q_Temp1))
                                 Q_temp2 = cursor.fetchone()
                                 print(Q_temp2["Q_Temp2"])
                                 Q_String = Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                 if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                    Status = "True"
                                 else:
                                    Status = "False"
                            Q_String= Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                            Q_String = Q_String.replace("{" , "")
                            Q_String = Q_String.replace("}" , "")
                            print(Q_String)
                        else:
                            Q_String = Q_String2.partition('<|>')[0]
                        print(Q_id, Q_String)
                        cursor.execute("""SELECT q.O_String, CtrlEnabled FROM gie151cb.dbo.Q_Options q INNER JOIN gie151cb.dbo.ResponseColumns r ON r.Q_ID=q.Q_ID WHERE Q_ID={}""".format(Q_id))
                        Response =cursor.fetchall()             
                #if (CtrlEnabled["CtrlEnabled"] is not None) and (CtrlEnabled["O_ReturnValue"] is not None):
                 #   cursor.execute("""SELECT COUNT(*) as i_count FROM gie151cb.InstCallDetails WHERE UNID='{}'""".format(UNID))
                  #  count = cursor.fetchone()
                   # if (count["i_count"]) > 0:
                    #    if(CtrlEnabled["CtrlEnabled"] == 'T'):

                     #    else if (CtrlEnabled["CtrlEnabled"] == 'B'):  

                      #  else:
                            #check for complex Dispositions
            i_count = 0
            V_skipped = 'N'
            #check for complex skiplogic
            if ( V_skipped != 'Y'):
                print("ComplexSkipLogic")
                i_count = 0
                if (profiles[0]["Q_CLogic"] == 'Y'):
                    cursor.execute("""Select count(*) as i_count from gie151cb.dbo.ComplexSkipLogic WHERE BaseQ = {} AND LogicType='Post'""".format(profiles[0]['Q_ScreenNo']))
                    skplogic = cursor.fetchall()
                    print(skplogic)
                    if(skplogic[0]["i_count"] > 0):
                       cursor.execute("""Select Logic as CS_Logic, SkipTo as CS_SkipTo from gie151cb.dbo.ComplexSkipLogic WHERE BaseQ = {} AND LogicType='Post'""".format(profiles[0]['Q_ScreenNo']))
                       curComplexSkip = cursor.fetchall()
                       print(curComplexSkip)
                       for d in curComplexSkip:
                            if ( V_skipped != 'Y'):
                                i_count = 0
                                cursor.execute("""Select COUNT(*) as count FROM gie151cb.dbo.InstCallDetails WHERE {} AND UNID = '407500192391'""".format(d['CS_Logic']))
                                count_1 = cursor.fetchone()
                                print(count_1)
                                if(count_1["count"] > 0):
                                    if  (curComplexSkip[0]["CS_SkipTo"] != 'me'):
                                        cursor.execute("""SELECT DemoTypeCode FROM gie151cb.dbo.Q_Master WHERE Q_ScreenNo={}""".format(d['CS_SkipTo']))
                                        dtcode = cursor.fetchall()
                                        if(dtcode[0][DemoTypeCode] == 3):
                                            cursor.execute("""SELECT Next_Q FROM gie151cb.dbo.Q_Master WHERE Q_ScreenNo={}""".format(d['CS_SkipTo']))
                                            skp = cursor.fetchall()
                                            cursor.execute("""SELECT m.Q_String,m.Q_ID FROM gie151cb.dbo.Q_Master m WHERE Q_ScreenNo= {}""".format(skp[0]["Next_Q"]))
                                            Q_Master = cursor.fetchall()
                                            Q_String1 =  Q_Master[0]["Q_String"]
                                            Q_String2 = Q_String1.replace("<AgentName>", "John")
                                            if (Q_String2.find("<|>")) > 0 :
                                                Q_String = Q_String2.partition('<|>')[0]
                                                print(Q_String)
                                            if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                                print("Found {}")
                                                Status = "True"
                                                while (Status == 'True'):
                                                    i_Start = Q_String.find("{")
                                                    i_End = Q_String.find('}',Q_String.find("{"))
                                                    slice_object = slice(i_Start+1,i_End)
                                                    Q_Temp1 = Q_String[slice_object]
                                                    cursor.execute("""SELECT Q_Temp2=COALESCE('{}','''') FROM gie151cb.dbo.Orglead WHERE UNID='407500192391'""".format(Q_Temp1))
                                                    Q_temp2 = cursor.fetchone()
                                                    print(Q_temp2["Q_Temp2"])
                                                    Q_String = Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                                    if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                                        Status = "True"
                                                    else:
                                                         Status = "False"
                                                    Q_String= Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                                    Q_String = Q_String.replace("{" , "")
                                                    Q_String = Q_String.replace("}" , "")
                                                    print(Q_String)
                                            else:
                                                Q_String = Q_String2.partition('<|>')[0]
                                                print(Q_id, Q_String)
                                            cursor.execute("""SELECT O_String, CtrlEnabled FROM gie151cb.dbo.Q_Options where Q_ID =(SELECT Q_ID FROM gie151cb.Q_Master WHERE Q_ScreenNo= {})""".format(profiles[0]["Next_Q"]))
                                            Response_1 =cursor.fetchall() 
                                            V_Skipped='Y'
                                        else:
                                            print(curComplexSkip[0]["CS_SkipTo"])
                                            if(curComplexSkip[0]["CS_SkipTo"] == '999'):
                                                Q_String = "Thank You!"
                                                Q_id = 999
                                                O_String  = None
                                                V_skipped = 'Y'
                                            else :
                                                cursor.execute("""SELECT Q_String,Q_ID  FROM gie151cb.dbo.Q_Master WHERE Q_ScreenNo={}""".format(d['CS_SkipTo']))   
                                                Q_Master = cursor.fetchall()
                                                Q_String1 =  Q_Master[0]["Q_String"]
                                                Q_String2 = Q_String1.replace("<AgentName>", "John")
                                                if (Q_String2.find("<|>")) > 0 :
                                                    Q_String = Q_String2.partition('<|>')[0]
                                                    print(Q_String)
                                                if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                                    print("Found {}")
                                                    Status = "True"
                                                    while (Status == 'True'):
                                                        i_Start = Q_String.find("{")
                                                        i_End = Q_String.find('}',Q_String.find("{"))
                                                        slice_object = slice(i_Start+1,i_End)
                                                        Q_Temp1 = Q_String[slice_object]
                                                        cursor.execute("""SELECT Q_Temp2=COALESCE('{}','''') FROM gie151cb.dbo.Orglead WHERE UNID='407500192391'""".format(Q_Temp1))
                                                        Q_temp2 = cursor.fetchone()
                                                        print(Q_temp2["Q_Temp2"])
                                                        Q_String = Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                                        if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                                            Status = "True"
                                                        else:
                                                            Status = "False"
                                                        Q_String= Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                                        Q_String = Q_String.replace("{" , "")
                                                        Q_String = Q_String.replace("}" , "")
                                                        print(Q_String)
                                                else:
                                                     Q_String = Q_String2.partition('<|>')[0]
                                                print(Q_id, Q_String)
                                   
                                                cursor.execute("""SELECT q.O_String, CtrlEnabled FROM gie151cb.dbo.Q_Options WHERE Q_ID=(SELECT Q_ID FROM gie151cb.dbo.Q_Master WHERE Q_ScreenNo={}""".format (d['CS_SkipTo']))
                                                Response =cursor.fetchall()
                                                V_skipped = 'Y'
                                    else:
                                        cursor.execute("""SELECT Q_String,Q_ID FROM gie151cb.dbo.Q_Master m WHERE Q_ScreenNo={}""".format(profiles[0]["Q_ScreenNo"]))
                                        Q_Master = cursor.fetchall()
                                        Q_String1 =  Q_Master[0]["Q_String"]
                                        Q_String2 = Q_String1.replace("<AgentName>", "John")
                                        if (Q_String2.find("<|>")) > 0 :
                                            Q_String = Q_String2.partition('<|>')[0]
                                            print(Q_String)
                                        if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                            print("Found {}")
                                            Status = "True"
                                            while (Status == 'True'):
                                                i_Start = Q_String.find("{")
                                                i_End = Q_String.find('}',Q_String.find("{"))
                                                slice_object = slice(i_Start+1,i_End)
                                                Q_Temp1 = Q_String[slice_object]
                                                cursor.execute("""SELECT Q_Temp2=COALESCE('{}','''') FROM gie151cb.dbo.Orglead WHERE UNID='407500192391'""".format(Q_Temp1))
                                                Q_temp2 = cursor.fetchone()
                                                print(Q_temp2["Q_Temp2"])
                                                Q_String = Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                                if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                                    Status = "True"
                                                else:
                                                    Status = "False"
                                            Q_String= Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                                            Q_String = Q_String.replace("{" , "")
                                            Q_String = Q_String.replace("}" , "")
                                            print(Q_String)
                                        else:
                                            Q_String = Q_String2.partition('<|>')[0]
                                        print(Q_id, Q_String)
                                   
                                        cursor.execute("""SELECT q.O_String, CtrlEnabled FROM gie151cb.dbo.Q_Options WHERE Q_ID=(SELECT Q_ID FROM gie151cb.dbo.Q_Master WHERE Q_ScreenNo={}""".format(profiles[0]["Q_ScreenNo"]))
                                        Response =cursor.fetchall()
                                        V_skipped = 'Y'

            if(V_skipped != 'Y'):
                print("skiplogic")
                if(profiles[0]['Next_Q'] is not  None):
                    cursor.execute("""SELECT Q_String,Q_ID FROM gie151cb.dbo.Q_Master m WHERE Q_ScreenNo={}""".format(profiles[0]["Next_Q"]))
                    Q_Master = cursor.fetchall()
                    print(Q_Master)
                    Q_String1 =  Q_Master[0]["Q_String"]
                    Q_String2 = Q_String1.replace("<AgentName>", "John")
                    if (Q_String2.find("<|>")) > 0 :
                        Q_String = Q_String2.partition('<|>')[0]
                        print(Q_String)
                    if (Q_String2.find("{")) > 0 and (Q_String2.find('}',Q_String2.find("{"),len(Q_String2) - 1)) > 0:
                        print("Found {}")
                        Status = "True"
                        while (Status == 'True'):
                            i_Start = Q_String.find("{")
                            i_End = Q_String.find('}',Q_String.find("{"))
                            slice_object = slice(i_Start+1,i_End)
                            Q_Temp1 = Q_String[slice_object]
                            cursor.execute("""SELECT Q_Temp2=COALESCE('{}','''') FROM gie151cb.dbo.Orglead WHERE UNID='407500192391'""".format(Q_Temp1))
                            Q_temp2 = cursor.fetchone()
                            print(Q_temp2["Q_Temp2"])
                            Q_String = Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                            if (Q_String.find("{")) > 0 and (Q_String.find('}',Q_String.find("{"),len(Q_String) - 1)) > 0:
                                Status = "True"
                            else:
                                Status = "False"
                            Q_String= Q_String.replace(Q_String[slice_object],Q_temp2["Q_Temp2"])
                            Q_String = Q_String.replace("{" , "")
                            Q_String = Q_String.replace("}" , "")
                            print(Q_String)
                    else:
                        Q_String = Q_Master[0]["Q_String"]
                        print(Q_id, Q_String)
                    cursor.execute("""SELECT Q_ID FROM gie151cb.dbo.Q_Master WHERE Q_ScreenNo = {}""".format(profiles[0]['Next_Q']))
                    Q_id_1 = cursor.fetchone()
                    print(Q_id_1['Q_ID'])
                    cursor.execute("""SELECT O_String, CtrlEnabled FROM gie151cb.dbo.Q_Options WHERE Q_ID= {}""".format(Q_id_1['Q_ID']))
                    response =cursor.fetchall()
                    print(response)

                    V_skipped = 'Y'

    except pymssql.Error as error:
        print("Failed to update record to database: {}".format(error))
            
    cursor.close()
    connection.close()

if __name__ == "__main__":
    next_question(5,"No (Tally as rejection)")