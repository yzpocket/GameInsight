$(document).ready(function () {

});

function critic_listing() {
    fetch('/critic_review')
      .then((res) => res.json())
      .then((data) => {
        let rows = data['result']
        console.log(rows)
        $('#section').empty()
        $('#section').append(`<div class="col row-cols-4 row-cols-md-1 g-0" id="cards-box">`)
        rows.forEach((a)=>{
              tmp_html = `<div class="card mb-3" style="max-height: auto;">
                <div class="row row-cols-2 g-0">
                  <div class="col-md-3 imagemargin" style="max-width: 135px;">
                    <img src="${a['image']}" class="img-fluid rounded-start" >
                  </div>
                  <div class="col-md-9">
                    <div class="card-body">
                      <h5 class="card-title">${a['title']}</h5>
                      <p class="card-text">${'★'.repeat(a['star']) + '☆'.repeat(5-a['star']) + ' ('+ a['star']+'/5)'}</p>
                      <p class="card-text ellipsis">${a['comment']}</p>
                      <p class="card-text"><small class="text-muted">-commenter</small></p>
                    </div>
                  </div>
                </div>`
            $('#cards-box').append(tmp_html)
        })
      })
}

