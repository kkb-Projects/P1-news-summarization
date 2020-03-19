function fillOutput(result){
}

$("#button").click(()=>{
    showSummary();
});

function renderOutput(result){
    $("#output").text(result.content);
}

function showSummary(){
    let title = $("#input-title").val();
    let body = $("#input-body").val();
    $.ajax({
        url:"summary",
        type: "post",
        dataType: "json",
        data: {"title":title, "body":body},
        success: (response)=>{
            window.location.hash = "#button";
            renderOutput(response.data);
        }
    });

}