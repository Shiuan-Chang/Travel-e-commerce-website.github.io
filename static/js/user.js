document.getElementById('headerContainer').innerHTML = header;
let loginPopup = document.querySelector(".loginPopup");
let signupPopup = document.querySelector(".signupPopup");
let loginPopupsignup = document.querySelector(".loginPopup-signup");
let signupPopuplogin = document.querySelector(".signup-Popuplogin");
let signupForm = document.querySelector(".signupForm");
let loginform = document.querySelector(".loginform");
//顯示登入畫面
document.querySelector(".signin_text").addEventListener("click", () => {
  loginPopup.style.display = "block";
});
//顯示註冊畫面
document.querySelector(".signup_text").addEventListener("click", () => {
  signupPopup.style.display = "block";
});
//關閉登入畫面
document.querySelector("#loginCloseButton").addEventListener("click", () => {
  loginPopup.style.display = "none";
});
//關閉註冊畫面
document.querySelector("#signupCloseButton ").addEventListener("click", () => {
  signupPopup.style.display = "none";
});
//從登入畫面點擊到註冊畫面
loginPopupsignup.addEventListener("click", () => {
  loginPopup.style.display = "none";
  signupPopup.style.display = "block";
});
//從註冊畫面點擊到登入畫面
signupPopuplogin.addEventListener("click", () => {
  signupPopup.style.display = "none";
  loginPopup.style.display = "block";
});

//會員註冊
let api_signup = "/api/user";

signupForm.addEventListener("submit", (e) => {
  e.preventDefault();
  let signup_note = document.querySelector(".signup_note");
  let signup_name = document.querySelector("#signup-name");
  let signup_email = document.querySelector("#signup-email");
  let signup_password = document.querySelector("#signup-password");
  fetch(api_signup, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: signup_name.value,
      email: signup_email.value,
      password: signup_password.value,
    }),
  })

    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"]) {
        signup_note.textContent = data["message"];
        signup_note.classList.add("warming");
        signupForm.style.height = "350px";
        return;
      }
      signup_note.textContent = "註冊成功，請重新登入";
      signup_note.classList.remove("warming");
      signup_note.classList.add("hint");
      signupForm.style.height = "350px";
      signup_name.value = "";
      signup_email.value = "";
      signup_password.value = "";
    });
});
//會員登入
let api_user_auth = "/api/user/auth"
loginform.addEventListener("submit", (e) => {
  e.preventDefault();
  let login_email = document.querySelector("#login_email");
  let login_pwd = document.querySelector("#login_pwd");
  fetch(api_user_auth, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: login_email.value,
      password: login_pwd.value,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"]) {
        document.querySelector(".login_note").textContent = data["message"];
        document.querySelector(".login_note").classList.add("warming");
        loginform.style.height = "295px";
        localStorage.removeItem('userToken');
      } else {
        localStorage.setItem('userToken', data['token']);
        location.reload();
      }
    });

});
//取得當前登入使用者的資料

window.addEventListener('pageshow', () => {
  checkToken();
});

function checkToken() {
  let token = localStorage.getItem('userToken');
  if (token) {
    verifyToken(token);
  } else {
    updateUIBasedOnToken(false);
  }
}

function verifyToken(token) {
  let headers = {
    'Content-Type': "application/json",
    'Authorization': 'Bearer ' + token
  };
  fetch(api_user_auth, {
    method: "GET",
    headers
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.data && data.data.id && data.data.name && data.data.email) {
        updateUIBasedOnToken(true);
      } else {
        updateUIBasedOnToken(false);
      }
      if (location.href.split("/")[3] == "booking") {
        getSchedule(data["data"]);
      }
    })
    .catch((error) => {
      // 當有錯誤發生，例如 API 請求失敗
      document.querySelector(".logbar").style.display = "block";
    });
}

function deleteUser() {
  fetch(api_user_auth, { method: "DELETE" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"]) {
        localStorage.removeItem('userToken');
        location.reload();
      }
    })
}

function updateUIBasedOnToken(isLoggedIn) {
  let logElement = document.querySelector(".log");
  let logbarElement = document.querySelector(".logbar");
  let signoutElement = logbarElement.querySelector('p[onclick="deleteUser();"]');

  if (isLoggedIn) {
    if (!signoutElement) {
      let signout = document.createElement("p");
      signout.textContent = "登出系統";
      signout.classList.add("logout-link");
      signout.setAttribute("onclick", "deleteUser();");
      logbarElement.insertBefore(signout, logElement);
    }
    logElement.style.display = "none";
  } else {
    if (signoutElement) {
      signoutElement.remove();
    }
    logElement.style.display = "block";
  }
}
