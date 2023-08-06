import damv1time7 as time7
import damv1time7.mylogger as Q
import damv1time7.mydump as D
import damv1manipulation as mpl

import re
import time
import stringcase

from .sandbox_mykubectl_series_1 import sanbox
cortex = sanbox()

class sandbox_series_2():

    # 2023-01-18 | new function for detected case of deployment name by podname
    def getJson_infoLabel_IoName_singlePods_by_podname_ns(self, _podname, _ns, _bShowCommandGtPoC = False):
        lst_ipoC = []
        get_bStatus_complete_sshcmd = False
        get_exception_message_handler = ''
        try:
            str_jsonpath =  '{.metadata.name}{", "}{.metadata.namespace}{", "}{.metadata.labels.app\.kubernetes\.io\/name}{", "}{.metadata.labels.pod-template-hash}'

            cmd_gtPoC = "kubectl get pods {podname} -n {ns} -o jsonpath='{c_jsonpath}' --sort-by=.metadata.name".format(podname =  _podname, ns = _ns, c_jsonpath = str_jsonpath)
            if _bShowCommandGtPoC==True: print(cmd_gtPoC)
            get_bStatus_complete_sshcmd, get_exception_message_handler, raw_datas = cortex.execsshcmd_detail_v2(cmd_gtPoC)
            if raw_datas==None:
                raise Exception('Please check your connection and try again [Fail of function "execsshcmd"]')
            else: 
                if len(raw_datas)!=0:
                    data_line = {}
                    lst_infpod = str(raw_datas).strip("']['").split(', ')
                    if "'list'" in str(type(lst_infpod)):
                        data_line['pod'] = str(lst_infpod[0])
                        data_line['namespace'] = str(lst_infpod[1])
                        data_line['labels component name'] = str(lst_infpod[2])
                        data_line['labels template hash'] = str(lst_infpod[3])
                    if len(data_line)>0: lst_ipoC.append(data_line)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getJson_infoLabel_IoName_singlePods_by_podname_ns"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, lst_ipoC

    # 2023-01-18 | new function for detected case of deployment name by podname
    def getJson_infoLabel_Component_singlePods_by_podname_ns(self, _podname, _ns, _bShowCommandGtPoC = False):
        lst_ipoC = []
        get_bStatus_complete_sshcmd = False
        get_exception_message_handler = ''
        try:
            str_jsonpath =  '{.metadata.name}{", "}{.metadata.namespace}{", "}{.metadata.labels.component}{", "}{.metadata.labels.pod-template-hash}'

            cmd_gtPoC = "kubectl get pods {podname} -n {ns} -o jsonpath='{c_jsonpath}' --sort-by=.metadata.name".format(podname =  _podname, ns = _ns, c_jsonpath = str_jsonpath)
            if _bShowCommandGtPoC==True: print(cmd_gtPoC)
            get_bStatus_complete_sshcmd, get_exception_message_handler, raw_datas = cortex.execsshcmd_detail_v2(cmd_gtPoC)
            if raw_datas==None:
                raise Exception('Please check your connection and try again [Fail of function "execsshcmd"]')
            else: 
                if len(raw_datas)!=0:
                    data_line = {}
                    lst_infpod = str(raw_datas).strip("']['").split(', ')
                    if "'list'" in str(type(lst_infpod)):
                        data_line['pod'] = str(lst_infpod[0])
                        data_line['namespace'] = str(lst_infpod[1])
                        data_line['labels component name'] = str(lst_infpod[2])
                        data_line['labels template hash'] = str(lst_infpod[3])
                    if len(data_line)>0: lst_ipoC.append(data_line)
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getJson_infoLabel_Component_singlePods_by_podname_ns"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, lst_ipoC

    def getLstEvents_fieldSelector_byDeployment(self, _deployment, _namespace, _bShowCommandGtPoC = False):
        lst_oput = []
        get_bStatus_complete_sshcmd = False
        get_exception_message_handler = ''
        try:
            cmd_gtEvent = "kubectl get events --field-selector involvedObject.name={deployment} -n {ns} --no-headers --sort-by='.lastTimestamp'".format(deployment = _deployment, ns = _namespace)
            cmd_awk = cmd_gtEvent + " | awk '{printf $1\" | \"$2\" | \"$3\" | \"$4\" | \"}{for(i=5;i<=NF;i++) printf $i\" \"; print \"\"}'"
            if _bShowCommandGtPoC==True: print(cmd_awk)
            get_bStatus_complete_sshcmd, get_exception_message_handler, raw_datas = cortex.execsshcmd_detail_v2(cmd_awk)
            if len(raw_datas) != 0 :
                lst_oput = raw_datas
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getLstEvents_fieldSelector_byDeployment"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, lst_oput

    def execRollout_restartDeployment(self, _deployment, _namespace, _bShowCommandGtPoC = False):
        lst_oput = []
        get_bStatus_complete_sshcmd = False
        get_exception_message_handler = ''
        try:
            cmd = "kubectl rollout restart deployment/{deployment} -n {ns}".format(deployment = _deployment, ns = _namespace)
            if _bShowCommandGtPoC==True: print(cmd)
            get_bStatus_complete_sshcmd, get_exception_message_handler, raw_datas = cortex.execsshcmd_detail_v2(cmd)
            if len(raw_datas) != 0 :
                lst_oput = raw_datas
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "execRollout_restartDeployment"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, lst_oput

    # from ast import literal_eval # Just for simulation
    def getEventsResponse_afterRestartDeployment_v2(self, _deployment, _namespace, _inCase, _bShowCommandGtPoC = False, _bShowResult = False, file = None):
        lst_oput = []
        response = False; 
        get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''
        event_podname = ''
        try:
            # # simulation sampling - - - - -
            # data = open('sample2.txt')
            # mainlist = [list(literal_eval(line)) for line in data]
            # lst_oput = mainlist[0]
            # # - - - - - - - - - - - - -
            get_bStatus_complete_sshcmd, get_exception_message_handler, lst_oput = self.getLstEvents_fieldSelector_byDeployment(_deployment, _namespace, _bShowCommandGtPoC)
            material_data = ''
            strfind_up = 'Scaled up replica set'
            strfind_down = 'Scaled down replica set'
            if len(lst_oput)!=0:
                lst_event_last_head2 = list(reversed(lst_oput))[0:2]
                # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                if len(lst_event_last_head2) == 1: # for only one list of event Scaled up
                    if _inCase == "event scaled up":
                        material_data = lst_event_last_head2[0].removesuffix('\n')
                        pattern = re.compile(r'{0}'.format(strfind_up))
                else:
                    # for only list of last event Scaled up
                    if re.search(re.compile(r'{0}'.format(strfind_up)), lst_event_last_head2[0].removesuffix('\n')) and _inCase == "event scaled up":  
                        material_data = lst_event_last_head2[0].removesuffix('\n')
                        pattern = re.compile(r'{0}'.format(strfind_up))
                    else:
                        if _inCase == "event scaled up":
                            material_data = lst_event_last_head2[-1:][0].removesuffix('\n')
                            pattern = re.compile(r'{0}'.format(strfind_up))
                        elif _inCase  == "event scaled down":
                            material_data = lst_event_last_head2[0].removesuffix('\n')
                            pattern = re.compile(r'{0}'.format(strfind_down))
                # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                if material_data != '':
                    row_split = material_data.split(" | ")
                    if len(row_split)!=0:
                        eTime = ''
                        eStatus = ''
                        eTask = ''
                        for idy, col in enumerate(row_split):
                            if idy == 0: eTime = col
                            if idy == 1: eStatus = col
                            if idy == 2: eTask = col
                            if idy == 4:
                                if re.search(pattern, col):
                                    lst_pods_events = mpl.string().getWord_searchString(col,_deployment)
                                    key = mpl.listofdictionary().getKeys_dictionary(lst_pods_events,0)
                                    if len(lst_pods_events)!=0:
                                        if _bShowResult == True:
                                            if file != None:
                                                D.printlf_dump_v1(True,'',file,' '*6, '{0}:'.format(str(stringcase.capitalcase(_inCase))))
                                                D.printlf_dump_v1(True,'',file,' '*7,' - {0}/{1}/{2}'.format(str(eTime),str(eStatus),str(eTask)))
                                                D.printlf_dump_v1(True,'',file,' '*7,' - ' + str(col))
                                                event_podname = str(lst_pods_events[0][int(key)])
                                                D.printlf_dump_v1(True,'',file,' '*7,' - event podname:', event_podname)
                                        response = True
                                    break
                    
                
                message = "EVENTS IS AVAILABLE"
            else:
                message = 'EVENTS IS NOT AVAILABLE'
            lst_oput.clear()
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "response_afterRestartDeployment"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, message, response, event_podname

    def wrapperRollout_restartDeployment(self, deployment, namespace, file, max_step):
        bBreak_rolloutDeployment = False; bBreak_stepEvent_ScaledUp = False; bBreak_stepEvent_ScaledDown = False
        response_rolloutRestart = False; response_scaledUp = False; response_scaledDown = False
        event_podname_scaledUp = ''; event_podname_scaledDown = ''
        nStep = 1
        data = {}
        lst_failed_sshexec = []
        while (nStep <= max_step):
            D.printlf_dump_v1(True,'', file, 'Buffer step time {0}'.format(str(nStep)))

            # skenario 1
            get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''; oput = []
            if nStep >= 1 and bBreak_rolloutDeployment == False:
                D.printlf_dump_v1(True,'', file,' '*6, 'Operation of Fn. execRollout_restartDeployment')
                get_bStatus_complete_sshcmd, get_exception_message_handler, \
                oput = self.execRollout_restartDeployment(deployment,namespace, False)
                D.printlf_dump_v1(True,'', file, ' '*8, '- bStatus_complete_sshcmd: ', str(get_bStatus_complete_sshcmd))
                D.printlf_dump_v1(True,'', file, ' '*8, '- exception_message_handler: ', str(get_exception_message_handler))
                D.printlf_dump_v1(True,'', file, ' '*8, '- Output: ', str(oput))
                bBreak_rolloutDeployment = True
                if len(oput)!=0:
                    if f'{deployment} restarted' in str(oput[0]): response_rolloutRestart = True
                if get_bStatus_complete_sshcmd == False:
                    data.clear()
                    data['identifier'] = 'execRollout_restartDeployment'
                    data['message'] = get_exception_message_handler
                    lst_failed_sshexec.append(data)
            get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''; oput.clear()

            # skenario 2
            get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''; message = ''; response = False
            inCase = 'event scaled up'
            if nStep >= 2 and bBreak_stepEvent_ScaledUp == False and response_rolloutRestart == True:  
                get_bStatus_complete_sshcmd, get_exception_message_handler, \
                message, response, event_podname_scaledUp = self.getEventsResponse_afterRestartDeployment_v2(deployment, namespace, inCase, False, True, file)
                D.printlf_dump_v1(True,'', file,' '*6, 'Operation of Fn. getEventsResponse_afterRestartDeployment_v2 --> {ic}:'.format(ic=inCase))
                D.printlf_dump_v1(True,'', file,' '*8, '- bStatus_complete_sshcmd:', str(get_bStatus_complete_sshcmd))
                D.printlf_dump_v1(True,'', file,' '*8, '- exception_message_handler:', str(get_exception_message_handler))
                D.printlf_dump_v1(True,'', file,' '*8, '- Message:', str(message))
                D.printlf_dump_v1(True,'', file,' '*8, '- Response:', str(response))
                if 'not available' in str(message).lower(): bBreak_stepEvent_ScaledUp = True
                else: bBreak_stepEvent_ScaledUp = response
                response_scaledUp = response
                if get_bStatus_complete_sshcmd == False:
                    data.clear()
                    data['identifier'] = 'getEventsResponse_afterRestartDeployment_v2 --> {ic}:'.format(ic=inCase)
                    data['message'] = get_exception_message_handler
                    lst_failed_sshexec.append(data)
            get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''; message = ''; response = False

            # skenario 3
            get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''; message = ''; response = False
            inCase = 'event scaled down'
            if nStep >= 3 and bBreak_stepEvent_ScaledDown == False and response_rolloutRestart == True:
                get_bStatus_complete_sshcmd, get_exception_message_handler, \
                message, response, event_podname_scaledDown = self.getEventsResponse_afterRestartDeployment_v2(deployment, namespace, inCase, False, True, file)
                D.printlf_dump_v1(True,'', file,' '*6, 'Operation of Fn. getEventsResponse_afterRestartDeployment_v2 --> {ic}:'.format(ic=inCase))
                D.printlf_dump_v1(True,'', file,' '*8, '- bStatus_complete_sshcmd:', str(get_bStatus_complete_sshcmd))
                D.printlf_dump_v1(True,'', file,' '*8, '- exception_message_handler:', str(get_exception_message_handler))
                D.printlf_dump_v1(True,'', file,' '*8, '- Message:', str(message))
                D.printlf_dump_v1(True,'', file,' '*8, '- Response:', str(response))
                if 'not available' in str(message).lower(): bBreak_stepEvent_ScaledDown = True
                else: bBreak_stepEvent_ScaledDown = response
                response_scaledDown = response
                if get_bStatus_complete_sshcmd == False:
                    data.clear()
                    data['identifier'] = 'getEventsResponse_afterRestartDeployment_v2 --> {ic}:'.format(ic=inCase)
                    data['message'] = get_exception_message_handler
                    lst_failed_sshexec.append(data)
            get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''; message = ''; response = False

            # skenario 4
            if nStep >= 4 and response_rolloutRestart == False and bBreak_stepEvent_ScaledUp == True and bBreak_stepEvent_ScaledDown == True:
                D.printlf_dump_v1(True,'', file,' '*6, 'No data in process')
                break
            if nStep >=4 and (response_rolloutRestart == True and response_scaledUp == True and response_scaledDown == True or response_rolloutRestart == False) :
                D.printlf_dump_v1(True,'', file,' '*6, 'Break')
                break
            
            time.sleep(2.8)
            nStep = nStep + 1

        D.printlf_dump_v1(True,'', file, 'Buffer step is closed')
        return response_rolloutRestart, response_scaledUp, response_scaledDown, lst_failed_sshexec, event_podname_scaledUp, event_podname_scaledDown

    def execute_wrapperRollout_restartDeployment(self, _namespace, _deployment, file):
        status_wrapper_completed = False
        get_exception_message_handler = ''

        res_rolloutrestart = False; res_slUp = False; res_slDown = False; lst_failed = []
        event_podname_scaledUp =''; event_podname_scaledDown = ''
        deployment_name = _deployment
        namespace_name = _namespace
        try:
            D.printlf_dump_v1(True,'', file,' '*6,'* '*29)
            D.printlf_dump_v1(True,'', file,' '*6,'WRAPPER ROLLOUT RESTART DEPLOYMENT [{0} -n {1}]'.format(str(deployment_name), str(namespace_name)))
            D.printlf_dump_v1(True,'', file,' '*6,'* '*29)

            res_rolloutrestart, res_slUp, res_slDown, lst_failed, event_podname_scaledUp, event_podname_scaledDown = self.wrapperRollout_restartDeployment(deployment_name, namespace_name, file, 20)

            if (res_rolloutrestart == True and res_slUp == True) or len(lst_failed)!= 0 :
                D.printlf_dump_v1(True,'', file,' '*6,'* '*29)
                if res_rolloutrestart == True and res_slUp == True and res_slDown == True:
                    D.printlf_dump_v1(True,'', file,' '*6,'STATUS: WRAPPER ROLLOUT RESTART DEPLOYMENT IS COMPLETE')
                elif res_rolloutrestart == True and res_slUp == True and res_slDown == False:
                    D.printlf_dump_v1(True,'', file,' '*6,'STATUS: PROCESS TAKES TOO LONG FOR SCALED DOWN')
                
                if len(lst_failed)!= 0 :
                    D.printlf_dump_v1(True,'', file,' '*6,'FAILED PROCESS OF WRAPPER ROLLOUT RESTART DEPLOYMENT:')
                    for rpt in lst_failed:
                        D.printlf_dump_v1(True,'', file,' '*6,str(rpt))
                D.printlf_dump_v1(True,'', file,' '*6,'* '*29)
            status_wrapper_completed = True
        except Exception as e:
            get_exception_message_handler = str(e)
            Q.logger(time7.currentTime7(),'Fail of function "execRollout_restartDeployment"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return status_wrapper_completed, get_exception_message_handler, res_rolloutrestart, res_slUp, res_slDown, lst_failed, event_podname_scaledUp, event_podname_scaledDown

    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Update for Type 'Restart-pod' | 27 Januari 2023
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getLst_pod_RestartedMore_by_ns(self, _namespace):
        lst_po = []
        get_bStatus_complete_sshcmd = False
        get_exception_message_handler = '' 
        try:
            cmd_gtpo = "kubectl get pods -n {0} --no-headers | sort --key 1 | awk '{1}'".format( _namespace, '$4 != "0" {print $1 " --> " $4}' )
            get_bStatus_complete_sshcmd, get_exception_message_handler, oput = cortex.execsshcmd_detail_v2(cmd_gtpo)
            if len(oput)!=0:
                for row in oput:
                    sp_ipo = str(row).split(" --> ")
                    lst_po.append(sp_ipo[0])
        except Exception as e:
            Q.logger(time7.currentTime7(),'Fail of function "getLst_info_allPods_by_ns"')  
            Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        return get_bStatus_complete_sshcmd, get_exception_message_handler, lst_po