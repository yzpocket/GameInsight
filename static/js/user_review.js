$(document).ready(function () {
    receive_rank();
    show_user_review();
});
function receive_rank() {
    fetch('/user_review').then(res => res.json()).then(data => {
        let games = data['result']
        games.forEach((a) => {
            let name = a['name']
            let num = a['num']

            let tmp_html = `<option value=${num}>${name}</option>`
            $('#inputGroupSelect01').append(tmp_html)
            $('#filter1').append(tmp_html)
        })

    })
}

function show_user_review() {
    fetch('/user_review2').then(res => res.json()).then(data => {
        let urs = data['result']
        console.log(urs)
        // $('#bucket-list').empty()
        urs.forEach((a) => {
            let name = a['gamename']
            let starnum = a['starnum']
            let review = a['review']
            let today = a['today'].substr(4, 17)
            let imgurl = a['imgurl']
            let stars = '⭐'.repeat(starnum)

            let tmp_html = `<div class = "mybox"> 
                                <div style="float: left; width: 15%">
                                    <img src="${imgurl}"
                                        style="width:150px; height:90px;" />
                                </div>
                                <div>
                                    <h4 class="card-title" style="float: left; width: 60%; text-align:left">${name}</h4>
                                    <p id="star_num" style="text-align:left">${stars}</p>
                                    <p style="float: left; width: 60%; text-align:left">${review}</p>
                                    <p style = "font-size: 12px;">${today}</p>
                                </div>
                            </div>`
            $('#ur-list').append(tmp_html)
        })

    })
}

function save_user_review() {
    let formData = new FormData();

    let gamename = $("select[id = inputGroupSelect01] option:selected").text()
    let starnum = $('#inputGroupSelect02').val()
    let review = $('#floatingTextarea').val()
    let today = new Date()

    formData.append("gamename_give", gamename);
    formData.append("starnum_give", starnum);
    formData.append("review_give", review);

    formData.append("today_give", today);

    fetch('/user_review', { method: "POST", body: formData, }).then((response) => response.json()).then((data) => {
        alert(data["msg"]);
        window.location.reload();
    });
}

function filter_show() {
    fetch('/user_review2').then(res => res.json()).then(data => {
        let urs = data['result']
        console.log(urs)
        $('#ur-list').empty()
        urs.forEach((a) => {
            let cnt = 0;

            let name = a['gamename']
            let starnum = a['starnum']
            let review = a['review']
            let today = a['today'].substr(4, 17)
            let imgurl = a['imgurl']
            let stars = '⭐'.repeat(starnum)

            let tmp_html = `<div class = "mybox"> 
                                <div style="float: left; width: 15%">
                                    <img src="${imgurl}"
                                        style="width:150px; height:90px;" />
                                </div>
                                <div>
                                    <h4 class="card-title" style="float: left; width: 60%; text-align:left">${name}</h4>
                                    <p id="star_num" style="text-align:left">${stars}</p>
                                    <p style="float: left; width: 60%; text-align:left">${review}</p>
                                    <p style = "font-size: 12px;">${today}</p>
                                </div>
                            </div>`
            if ($('#filter2').val() != "전체") {
                if (starnum != $('#filter2').val()) {
                    cnt++
                }
            }
            if ($('#filter1').val() != "전체") {
                if (name != $("select[id = filter1] option:selected").text()) {
                    cnt++
                }
            }
            console.log($("select[id = filter1] option:selected").text(), $('#filter2').val(), cnt)
            if (cnt == 0) {
                $('#ur-list').append(tmp_html)
            }
        })

    })
}