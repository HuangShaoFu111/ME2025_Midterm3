// orderadd.js

// 1. 選取商品種類後的連動邏輯 (Fetch API)
function selectCategory() {
    const category = document.getElementById("product-category").value;
    const productSelect = document.getElementById("product-name");
    
    // 清空並重置商品名稱選單
    productSelect.innerHTML = '<option value="" disabled selected>載入中...</option>';
    
    fetch(`/product?category=${encodeURIComponent(category)}`)
        .then(response => response.json())
        .then(data => {
            productSelect.innerHTML = '<option value="" disabled selected>請選擇商品</option>';
            data.product.forEach(item => {
                const option = document.createElement("option");
                option.value = item;
                option.textContent = item;
                productSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            productSelect.innerHTML = '<option value="" disabled selected>載入失敗</option>';
        });
}

// 2. 選取商品後的價格更新邏輯 (Fetch API)
function selectProduct() {
    const productName = document.getElementById("product-name").value;
    
    fetch(`/product?product=${encodeURIComponent(productName)}`)
        .then(response => response.json())
        .then(data => {
            const priceInput = document.getElementById("product-price");
            priceInput.value = data.price;
            countTotal(); // 取得價格後自動計算小計
        })
        .catch(error => console.error('Error fetching price:', error));
}

// 3. 計算小計邏輯
function countTotal() {
    const price = parseFloat(document.getElementById("product-price").value) || 0;
    const amount = parseInt(document.getElementById("product-amount").value) || 0;
    const totalInput = document.getElementById("product-total");
    
    totalInput.value = price * amount;
}

// 開啟與關閉Modal 
function open_input_table() {
    document.getElementById("addModal").style.display = "block";
}
function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}

function delete_data(value) {
    // 發送 DELETE 請求到後端 
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("伺服器回傳錯誤");
        }
        return response.json(); 
    })
    .then(result => {
        console.log(result);
        close_input_table();
        location.assign('/'); 
    })
    .catch(error => {
        console.error("發生錯誤：", error);
    });
}