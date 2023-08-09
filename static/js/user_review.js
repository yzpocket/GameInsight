$(document).ready(function () {
    receive_rank();
    show_user_review();
});
function receive_rank() {
    fetch('/user_review').then(res => res.json()).then(data => {
        let games = data['result']
        console.log(games)
        games.forEach((a) => {
            let name = a['name']
            let num = a['num']
            console.log(name)

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
            let today = a['today'].substr(4,17)
            let imgurl = a['imgurl']
            let stars = '⭐'.repeat(starnum)

            let tmp_html = `<div>
                                <div style="float: left;">
                                    <img src="${imgurl}"
                                        style="width:150px; height:90px;" />
                                </div>
                                <div>
                                    <h5 class="card-title" style="float: left; width: 30%;">${name}</h5>
                                    <p id="star_num">${stars}</p>
                                    <p class="mycomment">${review}</p>
                                    <p>${today}</p>
                                </div>
                            </div><br>`
            $('#bucket-list').append(tmp_html)
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
