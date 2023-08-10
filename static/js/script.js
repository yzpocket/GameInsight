$(document).ready(function () {
    const token = $.cookie('mytoken');
    if (token) {
        // 토큰이 존재하면 로그인한 상태로 간주하여 화면에 다른 내용을 표시할 수 있습니다.
        // 이에 맞게 로그아웃 버튼을 보이게하고, 로그인 버튼을 숨깁니다.
        $('#logout-button').show();
        $('#login-button').hide();
    } else {
        // 토큰이 없는 경우는 로그아웃 버튼을 숨기고, 로그인 버튼을 보이게 합니다.
        $('#logout-button').hide();
        $('#login-button').show();
    }
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
                window.location.href = '/login';  // 회원가입 성공 시 로그인 페이지로 이동
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