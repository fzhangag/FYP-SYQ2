
function getPanelContent(type){
    var str='';
    if(type=='calendar'){
        str+='<form class="layui-form layui-form-calendar" action="" style="margin:5% 10% 10%;">\n' +
            '            <div class="layui-form-item">\n' +
            '                <label class="layui-form-label">Date: </label>\n' +
            '                <div class="layui-input-block">\n' +
            '                  <input type="text" name="test1"  id="test1" placeholder="Please choose a date" autocomplete="off" class="layui-input">\n' +
            '                  <div id="testx" style="display:none"></div>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '</form>';
    }else if(type=='yes_or_no'){
        str+='<form class="layui-form layui-form-yes_or_no" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +
            '        <div class="layui-form-item">\n' +
            '          <div class="layui-input-inline" id="container">\n' +
            '          </div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</form>';
    }else if(type=='full_part'){
        str+='<form class="layui-form layui-form-full_part" action=" " style="margin:10% 5% 5%;">\n' +
            '    <div class="layui-form-item" >\n' +
            '<h4>Tpye of employment contract :</h4>\n' +
            '        <div class="layui-input-inline">\n' +
            '          <input type="radio" lay-filter="job_type" name="job_type" value="part_time" title="Part-time">\n' +
            '          <input type="radio" lay-filter="job_type" name="job_type" value="full_time" title="Full-time">\n' +
            '        </div>\n' +
            '    </div>\n' +
            '    <div class="layui-form-item" id="job_further_question" style="display: none">\n' +
            '        <h4>How many hours per week :</h4>\n' +
            '        <div class="layui-input-inline">\n' +
            '            <input type="number" name="hide_work_hr" id="work_hr" placeholder="How many hours per week" autocomplete="off" class="layui-input">\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</form>';
    }else if(type=='remote_specific'){
        str+='<form class="layui-form layui-form-remote_specific" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +
            '        <h4>Work Place :</h4>\n' +
            '        <div class="layui-input-inline">\n' +
            '          <input type="radio" lay-filter="remote_type"  name="remote_type" value="remote" title="Remote">\n' +
            '          <input type="radio" lay-filter="remote_type"  name="remote_type" value="specific_place" title="Specific Place">\n' +
            '        </div>\n' +
            '    </div>\n' +
            '    <div class="layui-form-item" style="display: none" id="remote_further_question">\n' +
            '          <h4>Address :</h4>\n' +
            '          <div class="layui-input-inline" >\n' +
            '             <input type="text" name="hide_specific_address" id="pac-input" required  lay-verify="required" placeholder="Enter your location" autocomplete="off" class="layui-input">\n' +
            '          <div id="map"></div>\n' +
            '          </div>\n' +
            '    </div>\n' +
            '</form>';

    }else if(type=='child_info'){
        str+='<form class="layui-form layui-form-child_info" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +
            '        <h4>Full Name :</h4>\n' +
            '        <div class="layui-input-inline">\n' +
            '          <input type="text" id="child_name" required  lay-verify="required" placeholder="Please choose a date" autocomplete="off" class="layui-input">\n' +
            '        </div>\n' +
            '    </div>\n' +
            '    <div class="layui-form-item">\n'+
            '        <h4>Date of Birth :</h4>\n' +
            '        <div class="layui-input-inline">\n' +
            '          <input type="text" id="test2" required  lay-verify="required"  placeholder="Please choose a date" autocomplete="off" class="layui-input">\n' +
            '        </div>\n' +
            '    </div>\n' +
            '    <div class="layui-form-item" style="display: none" id="university">\n' +
            '          <h4>Still study in university?</h4>\n' +
            '          <div class="layui-input-inline" >\n' +
            '            <input type="radio" lay-filter="university_y_n" name="hide_university_y_n" value="yes" title="Yes">\n' +
            '            <input type="radio" lay-filter="university_y_n" name="hide_university_y_n" value="no" title="No">\n' +
            '          </div>\n' +
            '    </div>\n' +
            '</form>';
    }else if(type=='child_further_info'){
            str+='<form class="layui-form layui-form-child_further_info" action=""  style="margin:5% 10% 10%;">\n' +
                '    <div class="layui-form-item">\n' +
                '        <h4>Custody : </h4>\n' +
                '        <div class="layui-input-inline">\n' +
                '          <input type="radio" lay-filter="child_Custody" name="child_Custody" value="Joint" title="Joint">\n' +
                '          <input type="radio" lay-filter="child_Custody" name="child_Custody" value="Sole" title="Sole">\n' +
                '        </div>\n' +
                '        </div>\n' +
                '    <div class="layui-form-item">\n' +
                '        <h4>Major Charge : </h4>\n' +
                '        <div class="layui-input-inline">\n' +
                '          <input type="radio" lay-filter="child_Charge" name="child_Charge" value="Father" title="Father">\n' +
                '          <input type="radio" lay-filter="child_Charge" name="child_Charge" value="Mother" title="Mother">\n' +
                '        </div>\n' +
                '    </div>\n' +
                '    <div class="layui-form-item">\n' +
                '        <div class="layui-form-item">\n' +
                '        <h4>Leave HK :  </h4>\n' +
                '          <div class="layui-input-inline">\n' +
                '            <input type="radio" lay-filter="leave_hk" name="leave_hk" value="yes" title="Yes">\n' +
                '            <input type="radio" lay-filter="leave_hk" name="leave_hk" value="no" title="No">\n' +
                '          </div>\n' +
                '        </div>\n' +
                '    </div>\n' +
                '    <div class="layui-form-item" style="display: none" id="leave_hk">\n' +
                '        <div class="layui-form-item">\n' +
                '             <h4>Where to live in future ? (Country or Region) </h4>\n' +
                '             <div class="layui-input-inline" >\n' +
                '                 <input type="text" name="hide_leave_place" id="leave_place" required  lay-verify="required" autocomplete="off" class="layui-input">\n' +
                '             </div>\n' +
                '        </div>\n' +
                '        <div class="layui-form-item">\n' +
                '             <h4>When start to live ?</h4>\n' +
                '             <div class="layui-input-inline" >\n' +
                '                 <input type="text" name="hide_test3" id="test3" required  lay-verify="required" placeholder="Please choose a date" autocomplete="off" class="layui-input">\n' +
                '             </div>\n' +
                '        </div>\n' +
                '     </div>\n' +
                '</form>';
    }else if(type=='child_main_info'){
             str+='\n' +
                 '<form class="layui-form layui-form-child_main_info" action=""  style="margin:5% 10% 10%;">\n' +
                 '    <div class="layui-form-item">\n' +
                 '        <h4>Maintenance</h4>\n' +
                 '        <div class="layui-input-inline">\n' +
                 '          <input type="radio" lay-filter="maintenance_y_n" name="maintenance_y_n" value="yes" title="Yes">\n' +
                 '          <input type="radio" lay-filter="maintenance_y_n" name="maintenance_y_n" value="no" title="No">\n' +
                 '        </div>\n' +
                 '    </div>\n' +
                 '    <div class="layui-form-item">\n' +
                 '        <h4>Can be modified in future?</h4>\n' +
                 '        <div class="layui-input-inline">\n' +
                 '          <input type="radio" lay-filter="modify_main_y_n" name="modify_main_y_n" value="yes" title="Yes">\n' +
                 '          <input type="radio" lay-filter="modify_main_y_n" name="modify_main_y_n" value="no" title="No">\n' +
                 '        </div>\n' +
                 '    </div>\n' +
                 '<div class="layui-form-item" style="display: none" id="maintainance">\n' +
                 '        <div class="layui-form-item">\n' +
                 '          <h4>Who will pay the child maintainance ?</h4>\n' +
                 '          <div class="layui-input-inline">\n' +
                 '            <input type="radio" lay-filter="who_main" name="hide_who_main" value="father" title="Father">\n' +
                 '            <input type="radio" lay-filter="who_main" name="hide_who_main" value="mother" title="Mother">\n' +
                 '          </div>\n' +
                 '        </div>\n' +
                 '        <div class="layui-form-item">\n' +
                 '          <h4>How much is the maintainance ? (per month)</h4>\n' +
                 '          <div class="layui-input-inline">\n' +
                 '             <input type="number" name="hide_main_amount" id="main_amount" required  lay-verify="required" placeholder="Please input number" autocomplete="off" class="layui-input">\n' +
                 '          </div>\n' +
                 '        </div>\n' +
                 '        <div class="layui-form-item">\n' +
                 '          <h4>When will the maintainance end ?</h4>\n' +
                 '          <div class="layui-input-inline">\n' +
                 '            <input type="radio" lay-filter="until_main" name="hide_until_main" value="university" title="University">\n' +
                 '            <input type="radio" lay-filter="until_main" name="hide_until_main" value="adult" title="18 years old">\n' +
                 '          </div>\n' +
                 '        </div>\n' +
                 '    </div>\n' +
                 '</form>';
    }else if(type=='spousal_'){
        str+='<form class="layui-form layui-form—spousal_" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +
            '        <div class="layui-form-item">\n' +
            '        <h4>Spousal Maintenance or not :</h4>\n' +
            '          <div class="layui-input-inline">\n' +
            '            <input type="radio" lay-filter="spousal_y_n" name="spousal_y_n" value="yes" title="Yes">\n' +
            '            <input type="radio" lay-filter="spousal_y_n" name="spousal_y_n" value="no" title="No">\n' +
            '          </div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '    <div class="layui-form-item" style="display: none" id="spousal_main">\n' +
            '        <div class="layui-form-item">\n' +
            '             <h4>Who will pay the spousal maintainance ?</h4>\n' +
            '             <div class="layui-input-inline" >\n' +
            '                 <input type="radio" lay-filter="spousal_who" name="hide_spousal_who" value="father" title="Husband">\n' +
            '                 <input type="radio" lay-filter="spousal_who" name="hide_spousal_who" value="mother" title="Wife">\n' +
            '             </div>\n' +
            '        </div>\n' +
            '        <div class="layui-form-item">\n' +
            '             <h4>What\'s the type of maintainance ?</h4>\n' +
            '             <div class="layui-input-inline" >\n' +
            '                 <input type="radio" lay-filter="spousal_type" name="hide_spousal_type" value="once" title="Lump Sum">\n' +
            '                 <input type="radio" lay-filter="spousal_type" name="hide_spousal_type" value="month" title="Monthly">\n' +
            '             </div>\n' +
            '        </div>\n' +
            '        <div class="layui-form-item">\n' +
            '             <h4>How much is the maintainance?</h4>\n' +
            '             <div class="layui-input-inline" >\n' +
            '                 <input type="number" name="hide_spousal_amount" id="spousal_amount" required  lay-verify="required" autocomplete="off" class="layui-input">\n' +
            '             </div>\n' +
            '        </div>\n' +
            '     </div>\n' +
            '</form>';

    }else if(type=='probation_'){
        str+='<form class="layui-form layui-form-probation_" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +
            '        <div class="layui-form-item">\n' +
            '        <h4>Is there a probation period for your job ?</h4>\n' +
            '          <div class="layui-input-inline">\n' +
            '            <input type="radio" lay-filter="prob_type" name="prob_type" value="yes" title="Yes">\n' +
            '            <input type="radio" lay-filter="prob_type" name="prob_type" value="no" title="No">\n' +
            '          </div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '    <div class="layui-form-item" style="display: none" id="proba_further_question">\n' +
            '        <div class="layui-form-item">\n' +
            '             <h4>How many weeks for probation ?</h4>\n' +
            '             <div class="layui-input-inline" >\n' +
            '                 <input type="number" name="hide_prob_time" id="prob_time" required  lay-verify="required" autocomplete="off" class="layui-input">\n' +
            '             </div>\n' +
            '        </div>\n' +
            '     </div>\n' +
            '</form>';

    }else if(type=='name_update'){
         str+='<form class="layui-form layui-form-name_update" action=""  style="margin:5% 10% 10%;">\n' +
             '    <div class="layui-form-item">\n' +
             '        <div class="layui-form-item">\n' +
             '          <div class="layui-input-block" id="container">\n' +
             '              <div class="layui-form-item">\n' +
             '                    <input type="text" class="layui-input" id="input_name" name="input_name" required placeholder="Please input the content here" style="width:300px;" />\n' +
             '              </div>\n' +
             '          </div>\n' +
             '        </div>\n' +
             '    </div>\n' +
             '</form>';
    }else if(type=='address'){
        str+='<form class="layui-form layui-form-address" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item" id="remote_further_question">\n' +
            '          <h4> Address:</h4><br>\n' +
            '          <div class="layui-input-inline" >\n' +
            '             <input type="text" name="address_input_field" id="pac-input" required  lay-verify="required" placeholder="Enter your location" autocomplete="off" class="layui-input">\n' +
            '          <div id="map"></div>\n' +
            '          </div>\n' +
            '    </div>\n' +
            '</form>';

    }else if(type=='couple'){
        str+='<form class="layui-form layui-form-couple" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +
            '        <div class="layui-form-item">\n' +
            '          <div class="layui-input-inline" id="container">\n' +
            '          </div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</form>';

    }else if(type=='asset'){
        str+=
            '<form class="layui-form layui-form-asset" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +

            '          <div class="layui-input-block" id="container">\n' +
            '           <div>\n'+
            '               <label  class="layui-form-label add_btn" style="background-color: #ccddff"> + </label>\n' +
            '               <input type="text" class="layui-input" name="asset_input" required placeholder="Please input the content here" style="width:300px;">\n' +
            '               <br>\n'+
            '           </div>\n'+
            '          </div>\n' +
            '    </div>\n' +
            '</form>';

    }

    return str;
}


function screen() {
	    var width = $(window).width();
	    if (width >=1200) {
	        return 3;   //L
	    } else if (width >=992) {
	        return 2;   //M
	    } else if (width >=768) {
	        return 1;   //S
	    } else {
	        return 0;   //XS
	    }
    }

$().ready(
    layui.use(['layer','element','laydate','form'], function(){
    //Start of layui.use
        var Total_Labor_Law_Question=21;
        var layer=layui.layer;
        var element=layui.element;
        var layuiJ = layui.jquery;
        var laydate=layui.laydate;
        var form=layui.form;
        var Message;
        var show=false;

        function displayPanel(str,btnName,response){
          layer.open({
           title:[response,'text-align: center'],
           type: 1,
           move:false,
           skin:'my-skin',
           closeBtn:0,
           shade: [0.8, '#F0F0F0'],
           content : str,
           btn:btnName,
           yes:function(index,layero){
                var msg='';
                var close=true;
                var arr=$("form").serializeArray();
                for(var i=2; i < arr.length; i++) {
                    if(arr[i]['value']==''){
                        if((arr[i]['name'].indexOf('hide')>-1&&show==true))
                            close=false;
                        if((arr[i]['name'].indexOf('hide')==-1&&show==false))
                            close=false;
                    }else{
                        msg+=arr[i]['value']+';';
                    }
                }
                if(close==true){
                    showUserMessage(msg);
                    sayToBot(msg);
                    show=false;
                    close=true;
                    layer.closeAll();
                }

           },success: function(layero, index){
                    this.enterConfirm = function(event){
                      if(event.keyCode === 13){
                        $(".layui-layer-btn0").click();
                        return false;
                      }
                    };
                    $(document).on('keydown', this.enterConfirm);
                },
                end: function(){
                    $(document).off('keydown', this.enterConfirm);
                },
           btnAlign : 'c',
           area: screen() < 2 ? ['90%','70%'] : ['50%','360px']
           });
        }

        function displayPanel_simple_type(str,btnName,response,mode){
            var msg='';
            var close=true;
            layer.open({
               title:[response,'text-align: center'],
               type: 1,
               move:false,
               skin:'my-skin',
               closeBtn:0,
               shade: [0.8, '#F0F0F0'],
               content : str,
               btn:btnName,
               yes:function(index,layero){
                   if(mode=='yes_no'){
                       msg+='yes';
                   }else if(mode=='couple'){
                       msg+='father';
                   }else if(mode=='name_update'){
                       var name=$('input_name').val();
                       if(name=='')
                           close=false;
                       else
                           msg+=name+";update";
                   }
                   if(close==true){
                       showUserMessage(msg);
                       sayToBot(msg);
                       layer.closeAll();
                   }

                },
               btn2:function(index,layero){
                   if(mode=='yes_or_no'){
                       msg+='no';
                   }else if(mode=='couple'){
                       msg+='mother';
                   }else if(mode=='name_update'){
                       var name=$('input_name').val();
                       if(name=='')
                           close=false;
                       else
                           msg+=name+";again";
                   }
                   if(close==true){
                       showUserMessage(msg);
                       sayToBot(msg);
                       layer.closeAll();
                   }
               },success: function(layero, index){
                    this.enterConfirm = function(event){
                      if(event.keyCode === 13){
                        // alert("Please choose your answer!");
                        return false;
                      }
                    };
                    $(document).on('keydown', this.enterConfirm);
                },
                end: function(){
                    $(document).off('keydown', this.enterConfirm);
                },
               btnAlign : 'c',
               area: screen() < 2 ? ['90%','70%'] : ['50%','360px']
               });
        }


        function initCanlendar(tagName){
                var tag='#'+tagName;
                if(tagName=='test2'){
                    laydate.render({elem: '#test2',lang: 'en',
                              done: function (value){
                                var birth = $("#test2").val().split('-');
                                var birthday = new Date(birth[0],birth[1]-1,birth[2]);
                                console.log(birthday.toString());
                                var nowdate = new Date();
                                var diffyear = parseInt(Math.abs((nowdate-birthday)/(1000*60*60*24*365)));
                                if (diffyear>=18){
                                        layuiJ('#university').show();
                                        show=true;
                                }else{
                                    layuiJ('#university').hide();
                                    show=false;
                                }
                              }
                        });
                }else{
                    laydate.render({elem: tag,lang: 'en'});
                }

        }

        $("#tt").click(function(e){

              var btnName_1=['Submit','Cancel'];
              var btnName_2=['Yes','No'];
              var btnName_3=['Update','Submit Again'];
              var btnName_4=['Father','Mother'];
              var str=getPanelContent('couple');
              var dic={'0':"Manager",'1':'Director'};
              displayPanel(create_job_title_panel(dic),btnName_1,"Hi there, nice to meet you!");

              // displayPanel_simple_type(str,btnName_4,"Hi there, nice to meet you!",'couple');
              // initCanlendar('test1');
              // initMap();
              form.render();
         });

         form.on('radio(job_type)', function(data){
            if(data.value=='full_time'){
                layuiJ('#job_further_question').show();
                show=true;
            }
            else{
                layuiJ('#job_further_question').hide();
                show=false;
            }
            form.render();
         });

         form.on('radio(remote_type)', function(data){
            if(data.value=='specific_place'){
                layuiJ('#remote_further_question').show();
                show=true;
            }
            else{
                layuiJ('#remote_further_question').hide();
                show=false;
            }
            form.render();
         });

         form.on('radio(maintenance_y_n)', function(data){
            if(data.value=='yes'){
                layuiJ('#maintainance').show();
                show=true;
            }
            else{
                layuiJ('#maintainance').hide();
                show=false;
            }
            form.render();
         });

         form.on('radio(leave_hk)', function(data){
            if(data.value=='yes'){
                layuiJ('#leave_hk').show();
                show=true;
            }
            else{
                layuiJ('#leave_hk').hide();
                show=false;
            }
            form.render();
         });

         form.on('radio(spousal_y_n)', function(data){
            if(data.value=='yes'){
                layuiJ('#spousal_main').show();
                show=true;
            }
            else{
                layuiJ('#spousal_main').hide();
                show=false;
            }
            form.render();
         });

        form.on('radio(prob_type)', function(data){
            if(data.value=='yes'){
                layuiJ('#proba_further_question').show();
                show=true;
            }
            else{
                layuiJ('#proba_further_question').hide();
                show=false;
            }
            form.render();
         });

        layuiJ(document).on('click','.add_btn',function(){    //Add Asset here
                $('#container').append(
                '<div>\n'+
                '<label  class="layui-form-label remove_btn" style="background-color: #ffb3cc"> - </label>\n'+
                '<input type="text" name="asset_input" class="layui-input" style="width:300px;" placeholder="Please input the content here">\n' +
                '<br>'+
                '</div>'
                );
                form.render();
        });

        layuiJ(document).on('click','.remove_btn',function(){ //Remove Asset here
                var list = document.getElementById('container');
                var length = list.childNodes.length - 1;
                list.removeChild(list.childNodes[length]);
                form.render();
        });


function checkDuplicateLayer(className){
    if($('.'+className).length>0)
        $('.'+className)[0].remove();
}



//-----------------------------------Default Chatbot Function-----------------------------------
function sayToBot(text){
    document.getElementById("msg_input").placeholder = "Type your messages here..."
    $.post("/chat",
            {
                text:text,
            },
            function(jsondata, status){
                if(jsondata["status"]=="success"){
                    //set percentage
                    var active = {
                       setPercent: function(){
                                var state=jsondata["state"];
                                if (isNaN(parseInt(state))==true) {
                                    state=0;
                                } else{
                                    if(state>Total_Labor_Law_Question)
                                        state=Total_Labor_Law_Question;
                                }
                                var p=(parseInt(state%(Total_Labor_Law_Question+1)*100/Total_Labor_Law_Question).toString()+'%');
                                element.progress('demo', p);
                            }
                        };
                     var othis = layuiJ(this);
                     active['setPercent'].call(this, othis);

                    //show response message
                    response=jsondata["response"];
                    if(response){
                        showBotMessage(response);
                    }

                    if(jsondata["job_title"]!=''){
                        dic = String(jsondata["job_title"]).split(";");
                    }
                    else{
                        dic = "";
                    }

                    //check if question is about date
                    if(jsondata['type']!=''){
                        var btnName_1=['Submit','Cancel'];
                        var btnName_2=['Yes','No'];
                        var btnName_3=['Update','Submit Again'];
                        var btnName_4=['Mother','Father'];
                        var calendarTag={'calendar':'test1','child_further_info':'test3'};
                        var btn_for_simple_panel={'yes_or_no':btnName_2,'name_update':btnName_3,'couple':btnName_4};
                        var str=getPanelContent(jsondata['type']);

                        checkDuplicateLayer('layui-form-'+jsondata['type']);

                        if(jsondata['type']=='calendar'||jsondata['type']=='child_further_info'){
                            displayPanel(str,btnName_1,response);
                            initCanlendar(calendarTag[jsondata['type']]);
                        }else if(jsondata['type']=='remote_specific'||jsondata['type']=='address'){
                            displayPanel(str,btnName_1,response);
                            initMap();
                        }else if(jsondata['type']=='child_info'){
                            displayPanel(str,btnName_1,response);
                            initCanlendar('test2');
                        }else if(jsondata['type']=='name_update'||jsondata['type']=='couple'||jsondata['type']=='yes_or_no'){
                            displayPanel_simple_type(str,btn_for_simple_panel[jsondata['type']],response,jsondata['type']);
                        }else if(jsondata['type']=='job'){
                            displayPanel(create_job_title_panel(dic),btnName_1,response);
                        }else{
                            displayPanel(str,btnName_1,response);
                        }
                        form.render();
                    }
                }
            });
}

function create_job_title_panel(dic){
    var temp='';
    for(var key in dic){
        temp+='<input type="radio" lay-filter="job_title" name="job_title" value="'+dic[key]+'" title='+dic[key]+'>\n';
    }

    str='<form class="layui-form layui-form-probation_" action=""  style="margin:5% 10% 10%;">\n' +
            '    <div class="layui-form-item">\n' +
            '        <div class="layui-form-item">\n' +
            '          <div class="layui-input-inline">\n' +temp+
            '          </div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</form>';
    return str;
}

$('.send_message').click(function (e) {
        msg = getMessageText();
        if(msg){
            showUserMessage(msg);
            sayToBot(msg);
            $('.message_input').val('');
        }
});

$('.message_input').keyup(function (e) {
    if (e.which === 13) {
        msg = getMessageText();
        if(msg){
        showUserMessage(msg);
        sayToBot(msg);
        $('.message_input').val('') ;
        }
    }
});

function addBr(text){
    return text.replace(/\n/g, "<br />");

}

Message = function (arg) {
    this.text = arg.text, this.message_side = arg.message_side;
    this.draw = function (_this) {
        return function () {
            var $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.message_side).find('.text').html(addBr(_this.text));
            $('.messages').append($message);
            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
};

function showBotMessage(msg){
        message = new Message({
             text: msg,
             message_side: 'left'
        });
        message.draw();
        $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
}

function showUserMessage(msg){
        $messages = $('.messages');
        message = new Message({
            text: msg,
            message_side: 'right'
        });
        message.draw();
        $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        $('#msg_input').val('');
}


getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };

$("#say").keypress(function(e) {
    if(e.which == 13) {
        $("#saybtn").click();
    }
});


//-----------------------------------end of layui.use---------------------------------------------
    })
);
