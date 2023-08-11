$(document).ready(function () {    

    critic_listing();
});
function show_critic_review() {
    // '/user_review'로 페이지 이동
    window.location.href = '/critic_review';
}

function critic_review_open(x){
    $('#critic_'+x).removeClass('ellipsis')
    $('#more_'+x).empty()
    tmp_html = `<a href="#" onclick="critic_review_close('${x}')">닫기</a>`
    $('#more_'+x).append(tmp_html)
  }
  
  function critic_review_close(x){
    $('#critic_'+x).addClass('ellipsis')
    $('#more_'+x).empty()
    tmp_html = `<a href="#" onclick="critic_review_open('${x}')">더보기</a>`
    $('#more_'+x).append(tmp_html)
  }
  
  function critic_listing() {
      fetch('/api/critic_review')
        .then((res) => res.json())
        .then((data) => {
          let rows = data['result']
          rows.forEach((a)=>{
                tmp_html = `<div class="card mb-3" style="max-height: auto;">
                  <div class="row row-cols-2 g-0">
                    <div class="col-md-3 imagemargin" style="max-width: 135px;">
                      <img src="${a['image']}" class="img-fluid rounded-start" >
                    </div>
                    <div class="col-md-9">
                      <div class="card-body">
                        <h5 class="card-title">${a['title']}</h5>
                        <p class="card-text">${'★'.repeat(a['star']) + '☆'.repeat(5-a['star']) + ' ('+ a['star']+'/5)'} | -${a['commenter']}</p>
                        <pre align="justify" class="card-text ellipsis"  id="critic_${a['no']}">${a['comment']} </pre>
                        <div class="row" id = "more_${a['no']}">
                          <a href="#" onclick="critic_review_open('${a['no']}')">더보기</a>
                        </div>
                        <p class="card-text"style="float:right"><small class="text-muted">${a['upload_time']}</small></p>
                      </div>
                    </div>
                  </div>`
              $('#cards-box').append(tmp_html)
          })
        })
  }
  
  function critic_showing() {
    $('#section').empty()
    tmp_html = `
    <div class="critic_review">
      <h5 style="float:left;margin-left:10px;margin-bottom:5px">게임 URL
          <label>
              <span style="float:left;margin-left:10px">
                  <a href="https://www.gamemeca.com/game.php" target="_blank">게임메카 링크</a>
              </span>
          </label>
      </h5>
      <div class="critic_review_block" >
          <input id="critic_url" type="email" class="form-control" placeholder="게임 메카에서 게임을 찾아보세요!">  
      </div>
      <h5 style="float:left;margin-left:10px;margin-bottom:5px"><label for="inputGroupSelect01">별점</label></h5>
      <div class="input-group critic_review_block" >
          <select class="form-select" id="critic_star">
              <option selected>-- 선택하기 --</option>
              <option value="1">⭐</option>
              <option value="2">⭐⭐</option>
              <option value="3">⭐⭐⭐</option>
              <option value="4">⭐⭐⭐⭐</option>
              <option value="5">⭐⭐⭐⭐⭐</option>
          </select>
      </div>
      <h5 style="float:left;margin-left:10px;margin-bottom:5px"><label for="floatingTextarea2">리뷰</label></h5>
      <div class="critic_review_block">
          <textarea id="critic_comment" class="form-control" style = "height:200px;" placeholder="리뷰를 남겨주세요!"></textarea>
          
      </div>
      
      <div class="mybtns">
          <button onclick="close_box()" type="button" class="btn btn-dark">기록하기</button>
      </div>
  </div>`
  $('#section').append(tmp_html)
  }
  
  function critic_posting() {
    let formData = new FormData()
    let url = $('#critic_url').val()
    let comment = $('#critic_comment').val()
    let star = $('#critic_star').val()
    formData.append('url_give', url)
    formData.append('comment_give', comment)
    formData.append('star_give', star)
    fetch('/api/critic_review', { method: 'POST', body: formData })
        .then((res) => res.json())
        .then((data) => {
          if(data['code']==-1){
            alert(data['msg'])
          }
          else if(data['code']==200){
            alert('저장되었습니다.')
            window.location.reload()
          }
            
        })
  }
  
  function close_box(){       
    var returnValue = confirm('저장하시겠습니까? 한 번 저장한 리뷰는 수정 및 삭제가 불가능합니다.')
    if (returnValue){
        critic_posting()
    }
    else{
        alert('취소되었습니다.')}
  }
  
  function critic_button_showing(){
    fetch('/api/logined',{method:'GET',})
    .then((res) => res.json())
    .then((data) => {
      if (data['result']=='success' && data['user_type'] == 1){
        $('#critic-button').show()
      }
      else{
        $('#critic-button').hide()
      }
    })
  }