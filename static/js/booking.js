
let bookingUrl = "/api/booking";
let infos = [];
//創建booking頁面
function processBooking(info) {
  if (info != null) {
    let main = document.querySelector("main");
    main.style.display = "block";
    let infoTime = info["time"] == "afternoon" ? "下午1點到晚上8點" : "早上9點到下午4點";
    let booking__logo = document.querySelector(".booking__logo");
    let container__date = document.querySelector(".container__date");
    let container__time = document.querySelector(".container__time");
    let container__cost = document.querySelector(".container__cost");
    let container__place = document.querySelector(".container__place");
    let confirm__total = document.querySelector(".confirm__total");
    let name = document.createTextNode(info["attraction"]["name"]);
    let date = document.createTextNode(info["date"]);
    let time = document.createTextNode(infoTime);
    let price1 = document.createTextNode(`新台幣 ${info["price"]} 元`);
    let price2 = document.createTextNode(`新台幣 ${info["price"]} 元`);
    let address = document.createTextNode(info["attraction"]["address"]);
    container__date.appendChild(date);
    booking__logo.appendChild(name);
    container__time.appendChild(time);
    container__cost.append(price1);
    confirm__total.appendChild(price2);
    container__place.appendChild(address);
    let bookingImg = document.createElement("img");
    bookingImg.src = info["attraction"]["image"];
    bookingImg.classList.add("bookingImg");
    let section__img = document.querySelector(".section__imgdiv");
    section__img.append(bookingImg);
    infos.push(
      info["price"],
      info["attraction"]["id"],
      info["attraction"]["name"],
      info["attraction"]["address"],
      info["attraction"]["image"],
      info["date"],
      info["time"]
    );
  } else {
    let no_plan = document.querySelector(".no_plan");
    no_plan.style.display = "block";
    let footer = document.querySelector(".footer");
    footer.classList.add("active");
  }
}
//取得資料創建headline
function getSchedule(userData) {
  if (userData == null) {
    location.href = "/";
    return;
  }
  let welcome = document.querySelector(".welcome");
  let welcomeText = document.createElement("p");
  welcomeText.textContent = `您好，${userData["name"]}，待預訂的行程如下：`;
  welcome.appendChild(welcomeText);
  let userName = document.querySelector("#name");
  let userEmail = document.querySelector("#email");
  userName.value = userData["name"];
  userEmail.value = userData["email"];
  const userToken = localStorage.getItem('userToken');
  fetch(bookingUrl, {
    method: "GET",
    headers: {
      "Authorization": "Bearer " + userToken
    }
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      let info = data["data"];
      processBooking(info);
    });
}
//建立預定行程，未登入則跳出登入視窗

window.reservation = function () {
  const userToken = localStorage.getItem('userToken');
  if (userToken) {
    location.href = "/booking ";
  } else {
    let loginPopup = document.querySelector('.loginPopup');
    loginPopup.style.display = "block";//將原先隱藏的登入畫面顯示出
  }
}

function buildSchedule(e) {
  e.preventDefault();
  const userToken = localStorage.getItem('userToken');
  if (!userToken) {
    let loginPopup = document.querySelector('.loginPopup');
    loginPopup.style.display = "block";
    return;
  }
  let selectDate = document.querySelector("#date");
  let selectTime = document.querySelector('input[name="selecttime"]:checked');
  if (!selectDate.value || !selectTime) {
    document.querySelector(".warning").textContent = "請輸入完整";
    return;
  }
  let price = selectTime.value === "morning" ? 2000 : 2500;
  let attractionId = location.href.split("/")[4];

  fetch(bookingUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + userToken
    },
    body: JSON.stringify({
      attractionId: attractionId,
      date: selectDate.value,
      time: selectTime.value,
      price: price,
    }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })

    .then((data) => {
      if (data["error"]) {
        if (data["error"] === "未登入系統，拒絕存取") {
          let loginPopup = document.querySelector('.loginPopup');
          loginPopup.style.display = "block";
        }

      } else if (data["ok"]) {
        window.location.href = `/booking`;
      }
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error.message);
    });
}

//刪除行程
function deleteSchedule() {
  const userToken = localStorage.getItem('userToken');
  fetch(bookingUrl, {
    method: "DELETE",
    headers: {
      "Authorization": "Bearer " + userToken
    }
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"]) {
        let main = document.querySelector("main");
        main.style.display = "none";
        let no_plan = document.querySelector(".no_plan");
        no_plan.style.display = "block";
      }
    });
}
