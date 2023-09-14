let url = new URL(window.location.href);
const fetchAttraction = async () => {
  const result = await fetch(`/api${url.pathname}`);
  const data = await result.json();
  const attraction = data.data;
  createElement(attraction);
};
function createElement(attraction) {
  //處理img
  let imgurls = attraction.images;
  imgurls.forEach((imgurl) => {
    let img_div = document.querySelector(".img_div");
    let sliders = document.querySelector(".sliders");
    let img = document.createElement("img");
    let dot_span = document.createElement("span");
    dot_span.classList.add("dot");
    img.src = imgurl;
    img.classList.add("attraction-imgs");
    img_div.append(img);
    sliders.append(dot_span);
  });
  //創建頁面
  let right_div = document.querySelector(".right_div");
  let name = document.createElement("h3");
  let category_mrt = document.createElement("p");
  name.textContent = attraction.name;
  category_mrt.textContent = `${attraction.category} at ${attraction.mrt}`;
  right_div.insertBefore(name, right_div.children[0]);
  right_div.insertBefore(category_mrt, right_div.children[1]);
  let below_text = document.querySelector(".below_text");
  let description = document.createElement("p");
  description.textContent = attraction.description;
  below_text.classList.add("below_text");
  below_text.insertBefore(description, below_text.children[0]);
  let address = document.createElement("p");
  address.textContent = attraction.address;
  below_text.insertBefore(address, below_text.children[2]);
  let transport = document.createElement("p");
  transport.textContent = attraction.transport;
  below_text.insertBefore(transport, below_text.children[4]);
}

fetchAttraction().then(() => {
  let index = 0;
  const imgs = document.querySelectorAll(".attraction-imgs");
  const dots = document.querySelectorAll(".dot");
  let img_num = imgs.length;
  function show_attraction() {
    //當index超過照片總數時歸0
    if (index > img_num - 1) {
      index = 0;
    }
    //當index小於0時，變成最後一頁
    if (index < 0) {
      index = img_num - 1;
    }
    //先將所有照片都先不顯示
    for (i = 0; i < imgs.length; i++) {
      dots[i].classList.remove("active");
      imgs[i].style.display = "none";
    }
    //然後是只顯示目前頁面
    dots[index].classList.add("active");
    imgs[index].style.display = "block";
  }

  function Next() {
    index++;
    show_attraction();
  }
  function Prev() {
    index--;
    show_attraction();
  }
  let prev_btn = document.querySelector(".prev");
  prev_btn.addEventListener("click", () => {
    Prev();
  });
  let next_btn = document.querySelector(".next");
  next_btn.addEventListener("click", () => {
    Next();
  });
  show_attraction();
});

//更改費用
let dollar = document.querySelector(".dollar");
let morn_input = document.querySelector("#morning");
let noon_input = document.querySelector("#afternoon");
morn_input.addEventListener("change", () => {
  dollar.textContent = "2000";
});
noon_input.addEventListener("change", () => {
  dollar.textContent = "2500";
});

let date = new Date();
date.setHours(date.getHours() + 8);
let localISOTime = date.toISOString().slice(0, 10);

let dateInput = document.querySelector("#date");
dateInput.min = localISOTime;
