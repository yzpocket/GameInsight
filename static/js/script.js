$(document).ready(function () {
});

function join(){
    let user_name = $('#user_name').val()
    let user_id = $('#user_id').val()
    let user_password1 = $('#user_password1').val()
    let user_password2 = $('#user_password2').val() // 유효성 체크용
    let user_postcode = $('#user_postcode').val()
    let user_address1 = $('#user_address1').val()
    let user_address2 = $('#user_address2').val()
    let user_email = $('#user_email').val()
    let user_type = $('#user_type').val()
    console.log(user_type);

    let formData = new FormData();
    formData.append("user_name_give", user_name)
    formData.append("user_id_give", user_id)
    formData.append("user_password1_give", user_password1)
    formData.append("user_postcode_give", user_postcode)
    formData.append("user_address1_give", user_address1)
    formData.append("user_address2_give", user_address2)
    formData.append("user_email_give", user_email)
    formData.append("user_type_give", user_type)

    fetch('/join', { method: "POST", body: formData, }).then((response) => response.json()).then((data) => {
        alert(data["msg"]);
        // 브라우저 새로고침 추가
        window.location.reload();
    });
}