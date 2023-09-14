//腳本載body底部就不用先加載DOM事件
const listBar = document.querySelector('.list_bar');
const middleSection = document.querySelector('.middle_section');
// 建立左側按鈕和圖片
const divLeftArrowBox = document.createElement('div');
divLeftArrowBox.className = 'div_left_arrow_box';
const imgLeftArrow = document.createElement('img');
imgLeftArrow.className = 'img_left_arrow';
imgLeftArrow.src = '../static/image/default-left.png';

divLeftArrowBox.appendChild(imgLeftArrow);
divLeftArrowBox.addEventListener('click', function () {
  // 左側按鈕
  // 左側按鈕，使捷運名稱向左滾動，例如滾動50像素
  middleSection.scrollLeft -= 200;
});

// 插入到.list_bar的開頭
listBar.insertAdjacentElement('afterbegin', divLeftArrowBox);

// 建立右側按鈕和圖片
const divRightArrowBox = document.createElement('div');
divRightArrowBox.className = 'div_right_arrow_box';
const imgRightArrow = document.createElement('img');
imgRightArrow.className = 'img_right_arrow';
imgRightArrow.src = '../static/image/default_right.png';

divRightArrowBox.appendChild(imgRightArrow);
divRightArrowBox.addEventListener('click', function () {
  // 右側按鈕事件處理函數
  middleSection.scrollLeft += 200;
});

// 插入到.list_bar的尾部
listBar.appendChild(divRightArrowBox);
fetch('/api/mrts')
  .then(response => response.json())
  .then(data => {
    const middleSection = document.querySelector('.middle_section');

    // 處理API回應，生成捷運站名稱
    data.data.forEach(mrtName => {
      const div = document.createElement('div');
      div.className = 'mrt_name';
      div.textContent = mrtName;

      // 添加事件監聽器
      div.addEventListener('click', function () {
        searchForAttraction(mrtName);
      });

      middleSection.appendChild(div);
    });
    setTimeout(() => {
      middleSection.scrollLeft = 0;
    }, 0);
  })
  .catch(error => {
    console.error('Error fetching the API:', error);
  });
function searchForAttraction(name) {
  // 呼叫searchWithMRTName函數，進行搜尋
  searchWithMRTName(name);
}

function searchWithMRTName(mrtName) {
  // 將名稱填入搜索框
  const searchInput = document.querySelector('#search_attrs');
  searchInput.value = mrtName;

  // 更新keyword並進行搜尋
  keyword = mrtName;
  page = 0;
  gridbox.innerHTML = "";  // 清空原本的景點列表
  fetchattras();  // 呼叫搜尋函數
}

function updatePageWithSearchResults(data) {
  // 在這裡根據返回的data更新您的頁面内容
  const gridbox = document.querySelector('.gridbox');
  gridbox.innerHTML = ''; // 清空之前的搜索結果

  data.data.forEach(attraction => {
    const div = document.createElement('div');
    // 根據你的頁面設計更新每個景點的展示方式
    div.textContent = attraction.name;
    gridbox.appendChild(div);
  });
}