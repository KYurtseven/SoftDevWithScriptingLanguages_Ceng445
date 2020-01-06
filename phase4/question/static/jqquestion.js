var current_question;

var topiclist = [];
var selectedtopic;

var embedlist = [];
var selectedembed;

var choicelist = [];
var selectedchoice;


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateQuestionBody()
{
    var url = "/question/updbody";
    var id;
    data = $("#updatebodyform").serialize();

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#updatebodyform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        var qbodydiv;
        qbodydiv = $("#q_body");
        qbodydiv.html("");
        qbodydiv.append(fdata['body']);
        current_question['body'] = fdata['body'];
    })
}

function updateDate()
{
    var url = "/question/upddate";
    var id;
    data = $("#updatedateform").serialize();

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#updatedateform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        var qaskdiv;
        qaskdiv = $("#q_ask_date");
        qaskdiv.html("");
        if(fdata['ask_date'].length != 0)
        {
            qaskdiv.append("Ask Date: " + fdata['ask_date']);
            current_question['ask_date'] = fdata['ask_date'];
        }
        else
        {
            // It does not update ask date, if it is null.
            qaskdiv.append("Ask Date: None");
            current_question['ask_date'] = fdata['ask_date'];
        }
    })
}

function updateParent()
{
    var url = "/question/updparent";
    var id;
    data = $("#updateparentform").serialize();

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#updateparentform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        var qparentdiv;
        qparentdiv = $("#q_parent");
        qparentdiv.html("");
        if(fdata['parent'].length != 0)
        {
            qparentdiv.append("Parent: " + fdata['parent']);
            current_question['parent'] = fdata['parent'];
        }
        else
        {
            qparentdiv.append("Parent: None");
            current_question['parent'] = fdata['parent'];
        }
    })
}

function addTopic()
{
    var url = "/question/addtopic";
    var id;
    data = $("#addtopicform").serialize();
    
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#addtopicform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        id = data.success.id;

        topiclist[id] = {'t_id': id};
        topiclist[id]['body'] = fdata['body'];

        $("#topicstable").append("<tr></tr>");
        row = $("#topicstable tr:last");
        updatetopicrow(topiclist[id], row);
        // $("table").trigger("update");
    })
}

function updateTopic()
{
    var url = "/question/updtopic";
    var id;
    data = $("#updatetopicform").serialize();

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#updatetopicform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        id = $("#updatetopicform [name=t_id]").val();
        // select existing row
        row = $("#rowtopic" + id);
        topiclist[id] = {'t_id': id};
        topiclist[id]['body'] = fdata['body'];
        updatetopicrow(topiclist[id], row);
    })

}

function deletetopic(t_id, confirmed)
{
    var q = $("#q_id").val();
    $.getJSON('/question/deltopic/'+q + '/' + t_id,function (data) {
        if(data.result == 'Fail' )
            alert(data.reason);
        else
        {
			// remove row from table
			$("#rowtopic"+t_id).remove();
			// delete from model
			topiclist[t_id] = undefined;
		} 
	});
}

function loadquestion()
{
    var q = $("#q_id").val();
    $.getJSON('/question/getquestion',{q_id: q},  function(data){
        if (data.result != 'Success')  
            return;
        current_question = data.question;
    })
}

function loadtopiclist()
{
    var q = $("#q_id").val();
    $.getJSON('/question/topiclist', {q_id: q}, function(data) {
		if (data.result != 'Success')  
            return;
        for(var i in data.topics)
        {
            var v = data.topics[i];
            topiclist[v.t_id] = v;
        }
		updatetopiclistview();
	});
}

function updatetopiclistview()
{
    var row;
    // remove all rows from table
	$("#topicstable tr").remove();
    for(id in topiclist)
    {
        $("#topicstable").append("<tr></tr>")
		row = $("#topicstable tr:last")
		updatetopicrow(topiclist[id], row);
    }
    // TODO ?
    //$("table").trigger("update")
}

function updatetopicrow(topic, row)
{
    var id = topic.t_id;
    var cell;
    row.attr("id","rowtopic" + id);
    row.html("");
    row.append('<td class="body"></td>');
    
    cell = row.find("td:last");
    cell.html(topic.body);

    row.unbind("click").click(function() {
        var id = this.id.slice(8); // remove heading "rowtopic"
        if (selectedtopic == id) {  // reclick on selected
            selectedtopic = undefined;
            this.classList.remove('selectedrow');
            $("#selectedtopicid").attr('value', '');
            $("#updtopicbutton").attr('disabled',true);
            $("#deltopicbutton").attr('disabled',true);
        } else {
            if (selectedtopic)  {
                $("#rowtopic"+selectedtopic)
                .removeClass('selectedrow');
            }
            this.classList.add('selectedrow');
            selectedtopic = id;
            $("#selectedtopicid").attr('value', selectedtopic);
            $("#updtopicbutton").attr('disabled',false);
            $("#deltopicbutton").attr('disabled',false);
        }
    })
}

function loadembedlist()
{
    var q = $("#q_id").val();
    $.getJSON('/question/embedlist', {q_id: q}, function(data) {
		if (data.result != 'Success')  
            return;
        for(var i in data.embeds)
        {
            var v = data.embeds[i];
            embedlist[v.e_id] = v;
        }
		updateembedlistview();
	});
}

function updateembedlistview()
{
    var row;
    // remove all rows from table
	$("#embedstable tr").remove();
    for(id in embedlist)
    {
        $("#embedstable").append("<tr></tr>")
		row = $("#embedstable tr:last")
		updateembedrow(embedlist[id], row);
    }
    // TODO ?
    //$("table").trigger("update")
}

function updateembedrow(embed, row)
{
    var id = embed.e_id;
    var cell;
    row.attr("id","rowembed" + id);
    row.html("");
    row.append('<td class="id"></td>');
    
    cell = row.find("td:last");
    cell.html(embed.e_id);

    row.append('<td class="body"></td>');
    
    cell = row.find("td:last");
    cell.html(embed.body);

    row.unbind("click").click(function() {
        var id = this.id.slice(8); // remove heading "rowembed"
        if (selectedembed == id) {  // reclick on selected
            selectedembed = undefined;
            this.classList.remove('selectedrow');
            $("#selectedembedid").attr('value', '');
            $("#updembedbutton").attr('disabled',true);
            $("#delembedbutton").attr('disabled',true);
        } else {
            if (selectedembed)  {
                $("#rowembed"+selectedembed)
                .removeClass('selectedrow');
            }
            this.classList.add('selectedrow');
            selectedembed = id;
            $("#selectedembedid").attr('value', selectedembed);
            $("#updembedbutton").attr('disabled',false);
            $("#delembedbutton").attr('disabled',false);
        }
    })
}

function addEmbed()
{
    var url = "/question/addembed";
    var id;
    data = $("#addembedform").serialize();
    
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#addembedform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        id = data.success.id;

        embedlist[id] = {'e_id': id};
        embedlist[id]['body'] = fdata['body'];

        $("#embedstable").append("<tr></tr>");
        row = $("#embedstable tr:last");
        updateembedrow(embedlist[id], row);
        // $("table").trigger("update");
    })
}

function updateEmbed()
{
    var url = "/question/updembed";
    var id;
    data = $("#updateembedform").serialize();

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#updateembedform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        id = $("#updateembedform [name=e_id]").val();
        // select existing row
        row = $("#rowembed" + id);

        embedlist[id] = {'e_id': id};
        embedlist[id]['body'] = fdata['body'];

        updateembedrow(embedlist[id], row);
    })
}

function deleteembed(e_id, confirmed)
{
    var q = $("#q_id").val();
    $.getJSON('/question/delembed/'+q + '/' + e_id,function (data) {
        if(data.result == 'Fail' )
            alert(data.reason);
        else
        {
			// remove row from table
			$("#rowembed"+e_id).remove();
			// delete from model
			embedlist[e_id] = undefined;
		} 
	});
}

function loadchoicelist()
{
    var q = $("#q_id").val();
    $.getJSON('/question/choicelist', {q_id: q}, function(data) {
		if (data.result != 'Success')  
            return;
        for(var i in data.choices)
        {
            var v = data.choices[i];
            choicelist[v.c_id] = v;
        }
		updatechoicelistview();
	});
}

function updatechoicelistview()
{
    var row;
    // remove all rows from table
	$("#choicestable tr").remove();
    for(id in choicelist)
    {
        $("#choicestable").append("<tr></tr>")
		row = $("#choicestable tr:last")
		updatechoicerow(choicelist[id], row);
    }
}

function updatechoicerow(choice, row)
{
    var id = choice.c_id;
    var cell;
    row.attr("id","rowchoice" + id);
    row.html("");

    row.append('<td class="body"></td>');
    cell = row.find("td:last");
    cell.html(choice.body);

    row.append('<td class="pos"></td>');
    cell = row.find("td:last");
    cell.html(choice.pos);

    row.append('<td class="iscorrect"></td>');
    cell = row.find("td:last");
    cell.html(JSON.stringify(choice.iscorrect));

    row.unbind("click").click(function() {
        var id = this.id.slice(9); // remove heading "rowchoice"
        if (selectedchoice == id) {  // reclick on selected
            selectedchoice = undefined;
            this.classList.remove('selectedrow');
            $("#selectedchoiceid").attr('value', '');
            $("#updchoicebutton").attr('disabled',true);
            $("#delchoicebutton").attr('disabled',true);
        } else {
            if (selectedchoice)  {
                $("#rowchoice"+selectedchoice)
                .removeClass('selectedrow');
            }
            this.classList.add('selectedrow');
            selectedchoice = id;
            $("#selectedchoiceid").attr('value', selectedchoice);
            $("#updchoicebutton").attr('disabled',false);
            $("#delchoicebutton").attr('disabled',false);
        }
    })
}

function addChoice()
{
    var url = "/question/addchoice";
    var id;
    data = $("#addchoiceform").serialize();

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#addchoiceform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        id = data.success.id;

        choicelist[id] = {'c_id': id};
        choicelist[id]['body'] = fdata['body'].toUpperCase();
        choicelist[id]['pos'] = fdata['pos'].toUpperCase();
        if(fdata['iscorrect'].toUpperCase() === "TRUE")
            choicelist[id]['iscorrect'] = "TRUE";
        else
            choicelist[id]['iscorrect'] = "FALSE";
        
            $("#choicestable").append("<tr></tr>");
        row = $("#choicestable tr:last");
        updatechoicerow(choicelist[id], row);
    })
}

function updateChoice()
{
    var url = "/question/updchoice";
    var id;
    data = $("#updatechoiceform").serialize();

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});

    $.post(url,data,function(data){
        var fdata = {};
        var row;
        $("#updatechoiceform :input").each(function (id,val) {
            fdata[val.name] = val.value;
        });
        id = $("#updatechoiceform [name=c_id]").val();
        // select existing row
        row = $("#rowchoice" + id);

        choicelist[id] = {'c_id': id};
        choicelist[id]['body'] = fdata['body'];
        choicelist[id]['pos'] = fdata['pos'];
        choicelist[id]['iscorrect'] = fdata['iscorrect'];

        updatechoicerow(choicelist[id], row);
    })
}

function deletechoice(c_id, confirmed)
{
    var q = $("#q_id").val();
    $.getJSON('/question/delchoice/'+q + '/' + c_id,function (data) {
        if(data.result == 'Fail' )
            alert(data.reason);
        else
        {
			// remove row from table
			$("#rowchoice"+c_id).remove();
			// delete from model
			choicelist[c_id] = undefined;
		} 
	});
}

function getpdf()
{
    
    var q = $("#q_id").val();
   
    $.getJSON('/question/getpdf/'+q,function (data) {
        $('#questionimage').attr('src', '');
        d = new Date();
        $("#questionimage").attr('src', data.path + "?" + d.getTime());
    });
}


$(document).ready(function () {

    // TODO
    // index.html acilinca getquestion ve topiclist fonksiyonlarini cagirmaya
    // calisiyor. Bunun nedeni ikisinin de ayni parent template'i kullanmasi
    
    // TODO
    // choice'da --EMBED--ID ekleyince sayfayi yenilemeden fotograf gozukmuyor

    // update body cancel
    $("#updatebodyform [name=cancelbutton]").click(function() {
		$("#updatebodyblock").fadeOut();
		return false;
    });
    // update body submit
    $("#updatebodybutton").click(function(){
        $("#updatebodyblock").fadeIn();
        
        $("#updatebodyform :input").each(function (i, elem) {
            elem.value = current_question[elem.name];
        });
        
        $("#updatebodyform [name=actionbutton]").unbind();
		// bind new event
		$("#updatebodyform [name=actionbutton]")
			.text("Update")
			.click(function () {
				$("#updatebodyblock").fadeOut();
                updateQuestionBody();
                setTimeout(function(){
                    getpdf();
                },1000);
                
				return false;});
		return false;
    })
    // update date cancel
    $("#updatedateform [name=cancelbutton]").click(function() {
		$("#updatedateblock").fadeOut();
		return false;
    });
    // update date submit
    $("#updatedatebutton").click(function(){
        $("#updatedateblock").fadeIn();
        
        $("#updatedateform :input").each(function (i, elem) {
            elem.value = current_question[elem.name];
        });
        
        $("#updatedateform [name=actionbutton]").unbind();
		// bind new event
		$("#updatedateform [name=actionbutton]")
			.text("Update")
			.click(function () {
				$("#updatedateblock").fadeOut();
                updateDate();
                setTimeout(function(){
                    getpdf();
                },1000);
				return false;});
		return false;
    });
    // update parent cancel
    $("#updateparentform [name=cancelbutton]").click(function() {
		$("#updateparentblock").fadeOut();
		return false;
    });
    // update parent submit
    $("#updateparentbutton").click(function(){
        $("#updateparentblock").fadeIn();
        
        $("#updateparentform :input").each(function (i, elem) {
            elem.value = current_question[elem.name];
        });
        
        $("#updateparentform [name=actionbutton]").unbind();
		// bind new event
		$("#updateparentform [name=actionbutton]")
			.text("Update")
			.click(function () {
				$("#updateparentblock").fadeOut();
                updateParent();
                setTimeout(function(){
                    getpdf();
                },1000);
				return false;});
		return false;
    })
    // add topic cancel
    $("#addtopicform [name=cancelbutton]").click(function() {
        $("#addtopicblock").fadeOut();
        return false;
    });
    // add topic submit
    $("#addtopicbutton").click(function() {
		$("#addtopicblock").fadeIn();
		// cancel previous events
		$("#addtopicform [name=actionbutton]").unbind();
		// bind new event
		$("#addtopicform [name=actionbutton]")
			.text("Add")
			.click(function () {
				$("#addtopicblock").fadeOut();
                addTopic();
                setTimeout(function(){
                    getpdf();
                },1000);
				return false;});
		return false;
	});
    // update topic cancel
    $("#updatetopicform [name=cancelbutton]").click(function() {
        $("#updatetopicblock").fadeOut();
        return false;
    });
    // update topic submit
    $("#updtopicbutton").click(function() {
		if (! selectedtopic) 
            return;
        
		$("#updatetopicblock").fadeIn();
        // for all input elements of the form
		$("#updatetopicform :input").each(function (i, elem) {
            // updates topic body in popup form
            if(elem.name == "body")
                elem.value = topiclist[selectedtopic].body;
            else
                elem.value = current_question[elem.name];
        });
        
        $("#selectedtopicid").attr('value', selectedtopic);
		// cancel previous events
		$("#updatetopicform [name=actionbutton]").unbind();
		// bind new event
		$("#updatetopicform [name=actionbutton]")
			.text("Update")
			.click(function () {
				$("#updatetopicblock").fadeOut();
                updateTopic();
                setTimeout(function(){
                    getpdf();
                },1000);
				return false;});
		return false;
    });
    // delete topic cancel
	$("#deltopicnoanswer").click(function() {
		$("#deltopicblock").fadeOut();
		return false;
    });
    // delete topic submit
	$("#deltopicbutton").click(function() {
		if (! selectedtopic) 
            return;
       
		$("#deltopicblock .topic").text("'" + topiclist[selectedtopic].body + "'");
		$("#deltopicblock").fadeIn();
		$("#deltopicyesanswer").unbind();   // cancel previous events
		$("#deltopicyesanswer").click(function () {
            $("#deltopicblock").fadeOut();
            deletetopic(selectedtopic); 
            selectedtopic = undefined;    
            $("#updtopicbutton").attr('disabled',true);
            $("#deltopicbutton").attr('disabled',true);
            setTimeout(function(){
                getpdf();
            },1000);
            return false;});
		return false;
	});
    // add embed cancel
    $("#addembedform [name=cancelbutton]").click(function() {
        $("#addembedblock").fadeOut();
        return false;
    });
    // add embed submit
    $("#addembedbutton").click(function() {
		$("#addembedblock").fadeIn();
		// cancel previous events
		$("#addembedform [name=actionbutton]").unbind();
		// bind new event
		$("#addembedform [name=actionbutton]")
			.text("Add")
			.click(function () {
				$("#addembedblock").fadeOut();
                addEmbed();
                setTimeout(function(){
                    getpdf();
                },1000);
				return false;});
		return false;
    });
    // update embed cancel
    $("#updateembedform [name=cancelbutton]").click(function() {
        $("#updateembedblock").fadeOut();
        return false;
    });
    // update embed submit
    $("#updembedbutton").click(function() {
        if (! selectedembed) 
            return;
        
        $("#updateembedblock").fadeIn();
        //for all input elements of the form
        $("#updateembedform :input").each(function (i, elem) {
            // updates topic body in popup form
            if(elem.name == "body")
                elem.value = embedlist[selectedembed].body;
            else
                elem.value = current_question[elem.name];
        });
        
        $("#selectedembedid").attr('value', selectedembed);
        // cancel previous events
        $("#updateembedform [name=actionbutton]").unbind();
        // bind new event
        $("#updateembedform [name=actionbutton]")
            .text("Update")
            .click(function () {
                $("#updateembedblock").fadeOut();
                updateEmbed();
                setTimeout(function(){
                    getpdf();
                },1000);
                return false;});
        return false;
    });
    // delete embed cancel
	$("#delembednoanswer").click(function() {
		$("#delembedblock").fadeOut();
		return false;
    });
    // delete embed submit
	$("#delembedbutton").click(function() {
		if (! selectedembed) 
            return;
       
		$("#delembedblock .embed").text("'" + embedlist[selectedembed].body + "'");
		$("#delembedblock").fadeIn();
		$("#delembedyesanswer").unbind();   // cancel previous events
		$("#delembedyesanswer").click(function () {
            $("#delembedblock").fadeOut();
            deleteembed(selectedembed); 
            selectedembed = undefined;    
            $("#updembedbutton").attr('disabled',true);
            $("#delembedbutton").attr('disabled',true);
            setTimeout(function(){
                getpdf();
            },1000);
            return false;});
		return false;
    });
    
    // add choice cancel
    $("#addchoiceform [name=cancelbutton]").click(function() {
        $("#addchoiceblock").fadeOut();
        return false;
    });
    // add choice submit
    $("#addchoicebutton").click(function() {
        $("#addchoiceblock").fadeIn();
        // cancel previous events
        $("#addchoiceform [name=actionbutton]").unbind();
        // bind new event
        $("#addchoiceform [name=actionbutton]")
            .text("Add")
            .click(function () {
                $("#addchoiceblock").fadeOut();
                addChoice();
                setTimeout(function(){
                    getpdf();
                },1000);
                return false;});
        return false;
    });

    // update choice cancel
    $("#updatechoiceform [name=cancelbutton]").click(function() {
        $("#updatechoiceblock").fadeOut();
        return false;
    });
    // update choice submit
    $("#updchoicebutton").click(function() {
        if (! selectedchoice) 
            return;
        
        $("#updatechoiceblock").fadeIn();
        //for all input elements of the form
        $("#updatechoiceform :input").each(function (i, elem) {
            // updates choice body in popup form
            if(elem.name == "q_id")
                elem.value = current_question[elem.name];
            else
                elem.value = choicelist[selectedchoice][elem.name];
        });
        
        $("#selectedchoiceid").attr('value', selectedchoice);
        // cancel previous events
        $("#updatechoiceform [name=actionbutton]").unbind();
        // bind new event
        $("#updatechoiceform [name=actionbutton]")
            .text("Update")
            .click(function () {
                $("#updatechoiceblock").fadeOut();
                updateChoice();
                setTimeout(function(){
                    getpdf();
                },1000);
                return false;});
        return false;
    });

    // delete choice cancel
	$("#delchoicenoanswer").click(function() {
		$("#delchoiceblock").fadeOut();
		return false;
    });
    // delete choice submit
	$("#delchoicebutton").click(function() {
		if (! selectedchoice) 
            return;
        
		$("#delchoiceblock .choice").text("'" + choicelist[selectedchoice].body + "'");
		$("#delchoiceblock").fadeIn();
		$("#delchoiceyesanswer").unbind();   // cancel previous events
		$("#delchoiceyesanswer").click(function () {
            $("#delchoiceblock").fadeOut();
            deletechoice(selectedchoice); 
            selectedchoice = undefined;    
            $("#updchoicebutton").attr('disabled',true);
            $("#delchoicebutton").attr('disabled',true);
            setTimeout(function(){
                getpdf();
            },1000);
            return false;});
		return false;
    });



    // pdf submit
    $("#getpdfbutton").click(function(){
        getpdf();        
        return false;
    })


    loadquestion();
    loadtopiclist();
    loadembedlist();
    loadchoicelist();
    getpdf();
})