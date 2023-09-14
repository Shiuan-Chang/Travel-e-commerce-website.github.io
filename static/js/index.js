const footer = document.querySelector("footer");
const main = document.querySelector("main");
const gridbox = document.querySelector(".gridbox");
main.append(gridbox);
let keyword = "";
let page = 0;
let isfetching = false;
let isComposing = false;

// 擷取景點創立景點頁面
class Createstitle {
  constructor(name, images, mrt, category, id) {
    this.name = name;
    this.images = images;
    this.mrt = mrt;
    this.category = category;
    this.id = id;
  }
  create() {
    let griddiv = document.createElement("div")//創立html div物件
    griddiv.className = "griddiv";//給予創立的griddiv元素girddiv的CSS屬性
    griddiv.setAttribute("onclick", "selectid(this.id)")//設置dom事件屬性。當點擊griddiv會觸發delectid。selectid是一個function，將id作為參數並導向對應頁面
    //處理img
    griddiv.setAttribute("id", this.id)//將 griddiv 的 id 屬性設定為 this.id。

    //處理圖片
    let img = document.createElement("img");
    img.src = this.images;
    //處理景點名字name
    let attra_name_div = document.createElement("div");
    let attra_name_text = document.createElement("p");
    attra_name_div.className = "attradiv";
    attra_name_text.textContent = this.name;
    //處理mrt和category
    let mrtdiv = document.createElement("div");
    let mrt_text = document.createElement("p");
    let category_text = document.createElement("p");
    mrtdiv.className = "mrtdiv";
    mrt_text.textContent = this.mrt;
    category_text.textContent = this.category;
    //合併元素
    mrtdiv.append(mrt_text, category_text);
    attra_name_div.append(attra_name_text, mrtdiv);
    griddiv.append(img, attra_name_div, mrtdiv);
    gridbox.append(griddiv);
  }
}
//連線fetch到景點
function fetchattras() {
  if (page == null) {
    observer.unobserve(footer);
    return;
  }//page是null時停止觀察
  let apiurl = keyword//根據keyword建立API URL
    ? `/api/attractions?page=${page}&keyword=${keyword}`//條件為真的回應(ternary operator)
    : `/api/attractions?page=${page}`;//條件為假的回應
  if (isfetching === false) {//在上一次的請求還未完成之前，不會發出另一個請求。也就是說，===false時，即為確保之前的請求已完成，才會進行下一步請求。
    isfetching = true;//異步操作
    fetch(apiurl)//執行非同步http請求
      .then((response) => {
        return response.json();
      })
      .then((data) => {//前面解析後的json資料
        if (data["error"]) {
          gridbox.innerHTML = `沒有符合${keyword}的景點`;//DOM 元素的屬性，可以用來獲取或設置該元素的 HTML 內容
          isfetching = false;
          return;
        }
        let attras = data.data;//data中的data屬性，如json中的各個資料值
        for (let attra of attras) {
          let showpage = new Createstitle(
            attra.name,
            attra.images[0],
            attra.mrt,
            attra.category,
            attra.id
          );
          showpage.create();
        }
        //還有頁面，重新打開觀察
        page = data["nextPage"];
        observer.observe(footer);
        isfetching = false;
      })
      .catch((e) => {
        isfetching = false;
        alert("error");
      });
  }
}
let searchinput = document.querySelector("#search_attrs");
document.getElementById("Button").addEventListener("click", () => {
  //關鍵字搜尋前，先把觀察關掉
  observer.unobserve(footer);
  gridbox.innerHTML = "";
  keyword = document.querySelector("#search_attrs").value;
  page = 0;
  fetchattras();
});
let options = {
  rootMargin: "0px",
  threshold: 0.1,
};
//滾動載入功能
let callback = (entry) => {
  if (entry[0].isIntersecting) {
    if (page !== null) {
      fetchattras();
    }
  }
};
const observer = new IntersectionObserver(callback, options);
observer.observe(footer);
//enter可提交表單
searchinput.addEventListener("compositionstart", () => {
  isComposing = true;
});

searchinput.addEventListener("compositionend", () => {
  isComposing = false;
});

searchinput.addEventListener("keydown", function (event) {
  if (event.keyCode === 13 && !isComposing) {
    event.preventDefault();
    document.querySelector("#Button").click();
  }
});

//改變當前瀏覽器窗口的位置，導航到一個新的網頁。
function selectid(checkid) {
  window.location.href = `/attraction/${checkid}`;//window.location.href：用來獲取或設置當前瀏覽器窗口的 URL ;/attraction/${checkid} 使用模板字面量語法建立一個新的 URL 字串。這個字串基於固定的部分 /attraction/ 和變量的部分 ${checkid}（這部分將被替換為 checkid 參數的實際值）。→即導航到/attraction/id頁面
}
function searchWithMRTName(mrtName) {
  // 將名稱填入搜索框
  searchinput.value = mrtName;

  // 更新keyword並進行搜尋
  keyword = mrtName;
  page = 0;
  gridbox.innerHTML = "";  // 清空原本的景點列表
  fetchattras();  // 呼叫搜尋函數
}
fetchattras();
