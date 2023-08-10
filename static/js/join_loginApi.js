$(document).ready(function () {
    show_joinForm();
    show_loginForm();
});
function show_joinForm(){

}
function user_join(){
    let user_name = $('#user_name').val();
    let user_id = $('#user_id').val()
    let user_password1 = $('#user_password1').val()
    let user_password2 = $('#user_password2').val() // 유효성 체크용
    let user_postcode = $('#user_postcode').val()
    let user_address1 = $('#user_address1').val()
    let user_address2 = $('#user_address2').val()
    let user_email = $('#user_email').val()
    let user_type = $('input[name=user_type]').val()

    let formData2 = new FormData();
    formData2.append("user_name_give", user_name)
    formData2.append("user_id_give", user_id)
    formData2.append("user_password1_give", user_password1)
    formData2.append("user_postcode_give", user_postcode)
    formData2.append("user_address1_give", user_address1)
    formData2.append("user_address2_give", user_address2)
    formData2.append("user_email_give", user_email)
    formData2.append("user_type_give", user_type)

    fetch('/api/join', { method: "POST", body: formData2, }).then((response) => response.json()).then((data) => {
        alert(data["msg"]);
        // 브라우저 새로고침 추가
        window.location.reload();
    })

}

function show_loginForm(){

}


function user_login() {
    let user_id = $('#user_id_login').val();  
    let user_password1 = $('#user_password1_login').val();
    console.log(user_id, user_password1)
    console.log($('#user_id_login').val())
    console.log($('#user_password1_login').val())

    let formData = new FormData();
    formData.append("user_id_give", user_id);
    formData.append("user_password1_give", user_password1);
    console.log(user_id, user_password1, formData)
    console.log(formData.getAll("user_id_give"));
    console.log(formData.getAll("user_password1_give"));    
    if (user_id !== '' && user_password1 !== '') {
        fetch('/api/login', { method: "POST", body: formData })
            .then((response) => response.json())
            .then((data) => {
                if (data["result"] === "success") {
                    $('#loginModal').modal('hide'); // 유효성 검사 통과 시 모달 창 닫기
                    // window.location.reload();
                } else {
                    // 실패 메시지를 알림으로 나타내기
                    showErrorMessage(data["msg"]);
                }
            })
            .catch((error) => {
                console.error('Fetch error:', error);
            });
    } else {
        alert("Both Fields are required");
    }
}

// 실패 메시지를 알림으로 나타내는 함수
function showErrorMessage(message) {
    const notification = document.getElementById("notification");
    notification.innerText = message;
    notification.style.display = "block";
    setTimeout(() => {
        notification.style.display = "none";
    }, 3000); // 3초 후에 알림을 숨김
}

    //     $.ajax({  
    //         url:"/api/login",  
    //         method:"POST",  
    //         formData: {"user_id_give":user_id, "user_password1":user_password1},  
    //         success:function(formData){  
    //             alert(data);  
    //             if(data == 'No-data'){  
    //                 alert("Invalid Password!");  
    //             }else{  
    //                 // $('#loginModal').hide();  
    //                 // location.reload();  
    //             }  
    //         }
    //     });  
    // } else {  
    //     alert("Both Fields are required");
    // }  
