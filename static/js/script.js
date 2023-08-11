$(document).ready(function () {
    const token = $.cookie('mytoken');
    critic_button_showing();
    if (token) {
        // 토큰이 존재하면 로그인한 상태로 간주하여 화면에 다른 내용을 표시할 수 있습니다.
        // 이에 맞게 로그아웃 버튼을 보이게하고, 로그인 버튼을 숨깁니다.
        $('#logout-button').show();
        $('#login-button').hide();
        $('#join-button').hide();
    } else {
        // 토큰이 없는 경우는 로그아웃 버튼을 숨기고, 로그인 버튼을 보이게 합니다.
        $('#logout-button').hide();
        $('#login-button').show();
    }
    listing()
});

function show_register() {
    // '/register'로 페이지 이동
    window.location.href = '/register';
}

// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function register() {
    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: $('#user_id').val(),
            pw_give: $('#user_password').val(),
            email_give: $('#user_email').val(),
            name_give: $('#user_name').val(),
            post_give: $('#user_postcode').val(),
            addr1_give: $('#user_address1').val(),
            addr2_give: $('#user_address2').val(),
            type_give: $('input[name=user_type]:checked').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.');
                window.location.href = '/';  // 회원가입 성공 시 로그인 페이지로 이동
            } else {
                alert(response['msg']);  // 실패 시 메시지 표시
            }
        }
    });
}


// ['쿠키'라는 개념에 대해 알아봅시다]
// 로그인을 구현하면, 반드시 쿠키라는 개념을 사용합니다.
// 페이지에 관계없이 브라우저에 임시로 저장되는 정보입니다. 키:밸류 형태(딕셔너리 형태)로 저장됩니다.
// 쿠키가 있기 때문에, 한번 로그인하면 네이버에서 다시 로그인할 필요가 없는 것입니다.
// 브라우저를 닫으면 자동 삭제되게 하거나, 일정 시간이 지나면 삭제되게 할 수 있습니다.
function login() {
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: { id_give: $('#login_user_id').val(), pw_give: $('#login_user_password').val() },
        success: function (response) {
            if (response['result'] == 'success') {
                // 로그인이 정상적으로 되면, 토큰을 받아옵니다.
                // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장합니다.
                $.cookie('mytoken', response['token'], { path: '/' });

                alert('로그인 완료!')
                window.location.href = '/'; // 또는 window.location.reload();
            } else {
                // 로그인이 안되면 에러메시지를 띄웁니다.
                alert(response['msg'])
            }
        }
    })
}

// 로그아웃 함수입니다.
function logout() {
    $.removeCookie('mytoken', { path: '/' });
    alert('로그아웃 되었습니다.');
    window.location.href = '/';
}

// 로그인 버튼 클릭 시 login 함수 호출
$('#login-button').click(login);

function execPostCode() {
    new daum.Postcode({
        oncomplete: function(data) {
           // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

           // 도로명 주소의 노출 규칙에 따라 주소를 조합한다.
           // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
           var fullRoadAddr = data.roadAddress; // 도로명 주소 변수
           var extraRoadAddr = ''; // 도로명 조합형 주소 변수

           // 법정동명이 있을 경우 추가한다. (법정리는 제외)
           // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
           if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
               extraRoadAddr += data.bname;
           }
           // 건물명이 있고, 공동주택일 경우 추가한다.
           if(data.buildingName !== '' && data.apartment === 'Y'){
              extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName);
           }
           // 도로명, 지번 조합형 주소가 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
           if(extraRoadAddr !== ''){
               extraRoadAddr = ' (' + extraRoadAddr + ')';
           }
           // 도로명, 지번 주소의 유무에 따라 해당 조합형 주소를 추가한다.
           if(fullRoadAddr !== ''){
               fullRoadAddr += extraRoadAddr;
           }

           // 우편번호와 주소 정보를 해당 필드에 넣는다.
           console.log(data.zonecode);
           console.log(fullRoadAddr);
           
           
           
           $("[name=user_postcode]").val(data.zonecode);
           $("[name=user_address1]").val(fullRoadAddr);
           document.getElementById("user_address2").focus();
           /* document.getElementById('signUpUserPostNo').value = data.zonecode; //5자리 새우편번호 사용
           document.getElementById('signUpUserCompanyAddress').value = fullRoadAddr;
           document.getElementById('signUpUserCompanyAddressDetail').value = data.jibunAddress; */
       }
    }).open();
}





function listing() {
    fetch('/game_ranking').then((res) => res.json()).then((data) => {
        let rows = data['result']
        $('#game-rank').empty()
        rows.forEach(a => {
            let rank = a['rank']
            let icon_url = a['icon_url']
            let name = a['name']
            let company = a['company']
            let genre = a['genre']
            let pay = a['pay']
            
            let temp_html = `<tr class="ranking-table-rows">
                                <td>
                                    <id="game_rank"> <span class="rank red">${rank}</span>
                                </td>
                                <td>
                                    <img id="game_icon" class="game-icon" src="${icon_url}">
                                </td>
                                <td>
                                    <div id="game_name" class="game-name">${name}</a></div>
                                </td>
                                <td>
                                    <div class="game-info">
                                        <p id="game_company" class="company">${company}</a></p>
                                        <span id="game_genre">${genre}</span> |
                                        <span id="game_pay">${pay}</span>
                                    </div>
                                </td>
                            </tr>`
            $('#game-rank').append(temp_html)
        })
    })
}

