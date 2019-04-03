(function () {

        var requestUrl = null;
        function bindChangePager() {
            $('#idPagination').on('click','a',function () {
                var num = $(this).text();
                init(num);

            })
        }


//判断是否有点击编辑模式的函数
        function bindEditMode() {
//            先找到id值为idEditMpode按钮，绑定点击事件click，jquery里面事件都没有on
            $('#idEditMpode').click(function () {
//                引用对象本身,检查按钮对象是否有btn-warning的属性
                var editing = $(this).hasClass('btn-warning');
//                console.log(editing)
//                如果有btn-warning属性说明该属性已经点击了。那么执行退出编辑。移除属性
                if (editing){
                    $(this).removeClass('btn-warning');
                    $(this).text('进入编辑模式');
//                    定位#table_tb id的位置，从这个id往下找find，所有type=checked的标签。对其进行遍历
                    $('#table_tb').find(':checked').each(function () {
//                        找到type=checked的tr。
                        var $currentTr = $(this).parent().parent();
//                        带入到该编辑函数中
                         trOutEditMode($currentTr);
                    })
                } else {
//如果没有这个属性就是没被点击过，所以是进入编辑模式

                    $(this).addClass('btn-warning');
                    $(this).text('退出编辑模式')

                    $('#table_tb').find(':checked').each(function () {
                        var $currentTr = $(this).parent().parent();
                         trIntoEditMode($currentTr);
                    })
                }
            })

        }
//        判断勾选框编辑函数
        function bindCheckbox() {
//            将父元素table_tb的事件继承到type属性为checkbox的行中，绑定的事件为click，这样可以继承下去click事件
            $('#table_tb').on('click',':checkbox', function () {
                var $currentTr = $(this).parent().parent();
//                判断id为idEditMpode的按钮是有是编辑模式，为true就执行
                if ($('#idEditMpode').hasClass('btn-warning')) {
//                    进入编辑模式后判断选择框是否有checked，这个就是是否被选中返回true或者fash
                    var ck = $(this).prop('checked');
//                    找到点击的父标签至父标签
//                    var $currentTr = $(this).parent().parent();
//                    console.log($currentTr)
//                    $currentTr.addClass('success')
//                    如果有checked，也就是说被选中了
                    if (ck){
//                        console.log($(this))
//                        那么进入编辑模式，调用trIntoEditMode函数
                        console.log('进入编辑模式')
//                        $currentTr.addClass('success')
//                        将所选的框都带有input属性，将他的父辈的父辈的标签传过去
                        trIntoEditMode($currentTr);
                    } else {
                        console.log("退出编辑模式")
//                        $currentTr.removeClass('success')
                        trOutEditMode($currentTr);
                    }
                }
            })
        }
//转换格式函数
        String.prototype.format = function (kwargs) {
            // this ="laiying: {age} - {gender}";
            // kwargs =  {'age':18,'gender': '女'}
            var ret = this.replace(/\{(\w+)\}/g,function (km,m) {
                return kwargs[m];
            });
            return ret;
        };

//初始化函数，使用ajax向后台发送请求，json格式
        function init() {
            $.ajax({
                url: requestUrl,
                type: 'GET',
                dataType: 'JSON',
//                请求回来的得到的数据进行函数处理，result参数为得到的数据
                success:function (result) {
                    initGlobalData(result.global_dict);
                    initHeader(result.table_config);
                    initBody(result.table_config,result.data_list)

                }
            })

        }
//定义表头函数
        function initHeader(table_config) {
            /*
            table_config = [
                {
                    'q': 'id',
                    'title': 'ID',
                    'display':false
                },
                {
                    'q': 'name',
                    'title': '随便',
                    'display': true
                }
            ]
             */

             /*
            <tr>
                <th>ID</th>
                <th>用户名</th>
            </tr>
            */
//             创建tr元素，tr包括td，一个tr是一行
            var tr = document.createElement('tr');
//            循环配置文件将里面的title标签的值取出并且添加th赋值后添加到tr中
            $.each(table_config,function (k,item) {
                if(item.display){
                    var th = document.createElement('th');
                    th.innerHTML = item.title;
                    $(tr).append(th);
                }

            });
            $('#table_th').empty()
            $('#table_th').append(tr);
        }
//添加到网页内容传入配置文件和数据库中的查得的数据
        function initBody(table_config,data_list){
            $('#table_tb').empty()
//            首先遍历数据库返回的数据得到每行的数据
            $.each(data_list,function (k,row) {
                // row = {'cabinet_num': '12B', 'cabinet_order': '1', 'id': 1},
                var tr = document.createElement('tr');
//给每个行标记上数据的自增id号，添加改属性
                tr.setAttribute('row-id',row['id'])
//遍历配置文件
                $.each(table_config,function (i,colConfig) {
                   if(colConfig.display){
                       var td = document.createElement('td');
//重新该写一下得到的值用来甄别哪个是全局变量哪个是td内容，哪个不显示
                       /* 生成文本信息 */
                       var kwargs = {};
                       $.each(colConfig.text.kwargs,function (key,value) {
//如果字符串0至2，就是前两个字符是@@那么就是全局变量，需要单独处理
                           if(value.substring(0,2) == '@@'){
//                               取出值
                               var globalName = value.substring(2,value.length); // 全局变量的名称
//                               值对应的数据库字段，在返回的值中由row[key]的形式取值
//                               console.log(globalName)
//                               console.log(window[globalName])
                               var currentId = row[colConfig.q]; // 获取的数据库中存储的数字类型值
//                               用函数进行比对处理
//                               console.log(colConfig.q)
                               var t = getTextFromGlobalById(globalName,currentId);
                               kwargs[key] = t;
                           }
//                           如果是一个@那么就直接在传过来的数据库的键中取值
                           else if (value[0] == '@'){
                                kwargs[key] = row[value.substring(1,value.length)]; //cabinet_num
                           }else{
//                               如果没有@值直接取值
                                kwargs[key] = value;
                           }
                       });
//                       获取内容，把值渲染到页面上
                       var temp = colConfig.text.content.format(kwargs);
                       td.innerHTML = temp;
//                       console.log(temp)
//                       对属性进行处理
                       /* 属性colConfig.attrs = {'edit-enable': 'true','edit-type': 'select'}  */
//                       遍历属性得出值
                        $.each(colConfig.attrs,function (kk,vv) {
//                            如果属性中有一个@符号，那么对其进行切割，然后在数据库传过来的字典中找到值
                            if (vv[0] =='@'){
                                td.setAttribute(kk,row[vv.substring(1,vv.length)])
                            }else {
                                td.setAttribute(kk,vv);
                            }
                        });
//添加td到tr中
                       $(tr).append(td);
                   }
                });

                $('#table_tb').append(tr);
            });


            /*
            * [
            *   {'cabinet_num': '12B', 'cabinet_order': '1', 'id': 1},
            *   {'cabinet_num': '12B', 'cabinet_order': '1', 'id': 1},
            * ]
            *
            *   <tr>
                    <td>12B</td>
                    <td>1</td>
                </tr>
                <tr>
                    <td>12C</td>
                    <td>1</td>
                </tr>
            *
            * */

        }
//设置服务器资产类型的。导入参数global_dict,定义全局变量
        function initGlobalData(global_dict) {
//            k为device_type_choices': Myseting.device_type_choices,'device_status_choices': Myseting.device_status_choices
//
            $.each(global_dict,function (k,v) {
                // k = "device_type_choices"
                // v= [[0,'xx'],[1,'xxx']]
//                device_type_choices = 123;
//                定义全局变量的表达式，k全局变量的名，v全局变量对应的值是个列表
                window[k] = v;
//                console.log(k,v)
            })
        }
//
        function getTextFromGlobalById(globalName,currentId) {
            // globalName = "device_type_choices"
            // currentId = 1
//            声明变量
            var ret = null;
//            遍历上一个全局变量定义的列表
            $.each(window[globalName],function (k,item) {
//                得到的item是一个数组1 "上架"，跟前面获取到的currentId进行对比
//                console.log(item[0],item[1],currentId);
//                如果相等返回item[1]配置文件中的汉字，表名该资产的相关信息
                if(item[0] == currentId){
                    ret = item[1];
//                    该处return只是结束循环
                    return
                }
            });
//            返回ret值
            return ret;
        }
//        变更所选框的属性，接收传过来的父辈标签
        function trIntoEditMode($tr){
//            填充颜色
            $tr.addClass('success')
//            添加属性表示记录改行是否被编辑了
            $tr.attr('has-edit',true)
//            父辈的标签，查找他的子标签，然后遍历纸标签的行
            $tr.children().each(function () {
//      $(this)表示所有被遍历出来的纸标签，然后.attr查看是否有该属性。返回true或者fals
//                console.log($tr)
                var editEnable = $(this).attr('edit-enable');
//                取出传递过来的编辑类型变量
                var editType = $(this).attr('edit-type');
//                console.log($(this))
//                如果这个标签属性为true
                if(editEnable=='true'){
//                    如果编辑类型是select下拉框
//                    下拉框样式：
//                    <select value="默认值(1)">
//                           <option value="1">上线</option>
//                            <option value="2">下线</option>
//                             <option value="3">上架</option>
//                    <select>
                    if (editType == "select"){
//                        那么取出其变量名
                        var globalName = $(this).attr('global-name')
//                        取出其默认值
                        var origin = $(this).attr('origin')
//                        设置下来狂元素
                        var sel = document.createElement('select')
//                        设置classname的样式名
                        sel.className ='form-control';
//                        遍历全局变量中的列表内容
                        $.each(window[globalName],function (k1,v1) {
//                            每遍历一次创建option属性
                            var op = document.createElement('option')
//                            设置<option value="值">值在全局变量列表的0号位
                            op.setAttribute('value',v1[0]);
//                            console.log(v1[1])
//                            添加<option value="值">文本信息</option>
                            op.innerHTML=v1[1];
//                            将整个op添加到select标签中
                            $(sel).append(op)
                        })
//                        jquery方式给select标签添加默认值
                        $(sel).val(origin)
//                        用jquer方式将select添加到页面中
                        $(this).html(sel);

                    }else if (editType == "input"){
                    var innerText = $(this).text();
//                    创建一个input标签
                    var tag = document.createElement('input');
//                    设置input标签的样式名
                    tag.className ='form-control'
//                    input标签value属性的值是innerText，也就是将原有标签内容再填入到input中
                    tag.value = innerText;
//                    将tag填入html中，html可以将文本以属性的方式填到页面中。
                    $(this).html(tag);
                    }
//                    那么取出他的文本信息

                }
            })
        }
//        退出编辑模式后恢复文本信息
        function trOutEditMode($tr) {
//遍历tr子目录的td属性
            $tr.removeClass('success')
            $tr.children().each(function () {
//                查看属性是否有edit-enable
            var editEnable = $(this).attr('edit-enable');
            var editType = $(this).attr('edit-type');
            if (editEnable == 'true') {
                if (editType == 'select'){
//                    var globalName = $(this).attr('global-name')
//                    查找到下拉框呗选中的值
                    var newText = $(this).find("option:selected").text()
                    var newId = $(this).find("option:selected").val()
//另一种取值的方法
//                    var $select = $(this).children().first()
//                    var newId = $select .val()
//                    var newText = $select[0].selectedOptions[0].innerHTML;
//                    console.log(sel_text)

//                    console.log(sel_val)
                    $(this).html(newText);
//                    每次更改都新加一个属性来存储改变的键值，以后保存的时候过来取
                    $(this).attr('new-val',newId)
                }else if (editType == 'input'){

                   var $input = $(this).children().first();
                   //                    取出值
                   var inputValue = $input.val();
                   //                    再把值写入
                    $(this).attr('new-val',inputValue)
                   $(this).html(inputValue);
                   $(this).attr('new_val',inputValue);
                }

                }
            })
            }
//        全选
        function bindCheckAll() {
//            找到所有纸标签的选择
            $('#idCheckAll').click(function () {
                 $('#table_tb').find(':checkbox').each(function (){

                     if ($('#idEditMpode').hasClass('btn-warning')) {
                         if ($(this).prop("checked")){
                         }else {
                             $(this).prop("checked", true)
                            var $currenntTr = $(this).parent().parent()
                            trIntoEditMode($currenntTr)
                        }

                     } else {
                        $(this).prop("checked", true)
                        }

                 })
            })
        }


//反选
        function bindReverseAll() {
            $('#reverse').click(function () {
                $('#table_tb').find(':checkbox').each(function () {
                    if ($('#idEditMpode').hasClass('btn-warning')) {
                        if ($(this).prop("checked")) {
                            $(this).prop('checked', false)
                            var $currenntTr = $(this).parent().parent()
                            trOutEditMode($currenntTr)
                        } else {
                            $(this).prop('checked', true)
                            var $currenntTr = $(this).parent().parent()
                            trIntoEditMode($currenntTr)
                        }
                    } else {
                        if ($(this).prop("checked")){
                            $(this).prop('checked', false)
                        } else {
                            $(this).prop('checked', true)
                        }
                    }
                })
            })
        }


//取消
        function bindCancelAll() {
            $('#Cancel').click(function () {
                $('#table_tb').find(':checked').each(function () {
                    if ($('#idEditMpode').hasClass('btn-warning')){
                        $(this).prop('checked', false)
                        var $currenntTr = $(this).parent().parent()
                            trOutEditMode($currenntTr)
                    }else {
                        $(this).prop('checked', false)
                    }
                })
            })
        }
//        保存
       function bindSave() {
           $('#Save').click(function (){
              var postList = []
               $('#table_tb').find('tr[has-edit="true"]').each(function () {
                   var id = $(this).attr('row-id');
                   var temp = {}
                   temp['id'] =id
                   $(this).children('[edit-enable="true"]').each(function () {
                       var origin= $(this).attr('origin');
                       var newVal = $(this).attr('new-val');
//                       console.log(newVal)
                       var name = $(this).attr('name');
//                       console.log(newVal)
                       if (origin != newVal) {
//                           list_data[newVal] = new_val;
                           temp[name] = newVal;
//                           temp[id] = id
//                           post_list.append(temp)
                        } else {
                       }
                   })
                   postList.push(temp)

           })
               // var jsonData = JSON.stringify(post_list);
//                 console.log(jsonData)
               $.ajax({
                    url:requestUrl,
                    type: 'PUT',
                    data: {'post_list': JSON.stringify(postList)},
                    dataType: 'JSON',
                    success:function (result) {
                        if(result.status){
                            init(1);
                        }else{
                            alert(result.error);
                        }
                    }
                })


           })
       }

        jQuery.extend({
            'NB': function (url) {
                requestUrl = url;
                init();
                bindEditMode();
                bindCheckbox();
                bindCheckAll();
                bindCancelAll();
                bindReverseAll();
                bindSave();
                bindChangePager();
            },
            'changePager': function (num) {
                init(num);
            }
        })
})();