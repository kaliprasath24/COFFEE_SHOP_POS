let bill = {};
let gstEnabled = false;

/*function addItem(name, price)
{
    if (!bill[name]) bill[name] = { qty: 0, price: price};
    bill[name].qty++;
    updateBill();
}*/

function addItem(name, price) {
    console.log("ITEM CLICKED:", name, price);

    if (!bill[name]) {
        bill[name] = { qty: 1, price: price };
    } else {
        bill[name].qty += 1;
    }

    updateBill();
}


function updateBill() {
    console.log("updateBill called", bill);

    let table = document.getElementById("billtable");
    if (!table) {
        console.error("billtable not found");
        return;
    }

    table.innerHTML = `
        <tr>
            <th>Item</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Total</th>
        </tr>
    `;

    let subtotal = 0;

    for (let item in bill) {
        let total = bill[item].qty * bill[item].price;
        subtotal += total;

        table.innerHTML += `
            <tr>
                <td>${item}</td>
                <td>
                    <button onclick="changeQty('${item}', -1)">−</button>
                    ${bill[item].qty}
                    <button onclick="changeQty('${item}', 1)">+</button>
                </td>
                <td>₹${bill[item].price}</td>
                <td>₹${total}</td>
            </tr>
        `;
    }

    let gstEnabled = document.getElementById("gstToggle").checked;
    let gst = gstEnabled ? subtotal * 0.05 : 0;

    document.getElementById("subtotal").innerText = subtotal.toFixed(2);
    document.getElementById("gst").innerText = gst.toFixed(2);
    document.getElementById("total").innerText = (subtotal + gst).toFixed(2);
}


/*function updateBill() {
    console.log("updateBill called", bill);

    let table = document.getElementById("billtable");
    if (!table) {
        console.error("billtable not found");
        return;
    }

    table.innerHTML = `
        <tr>
            <th>Item</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Total</th>
        </tr>
    `;

    let subtotal = 0;

    for (let item in bill) {
        let qty = bill[item].qty;
        let price = bill[item].price;
        let total = qty * price;
        subtotal += total;

        table.innerHTML += `
            <tr>
                <td>${item}</td>
                <td>
                    <button onclick="changeQty('${item}', -1)">-</button>
                    ${qty}
                    <button onclick="changeQty('${item}', 1)">+</button>
                </td>
                <td>₹${price}</td>
                <td>₹${total}</td>
            </tr>
        `;
    }

    let gstEnabled = document.getElementById("gstToggle").checked;
    let gst = gstEnabled ? subtotal * 0.05 : 0;

    document.getElementById("subtotal").innerText = subtotal.toFixed(2);
    document.getElementById("gst").innerText = gst.toFixed(2);
    document.getElementById("total").innerText = (subtotal + gst).toFixed(2);
}*/



/*function updateBill() {
    console.log("updateBill called", bill);
    let table = document.getElementById("billtable");

    // table header (once)
    table.innerHTML = `
        <tr>
            <th>Item</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Total</th>
        </tr>
    `;

    let subtotal = 0;

    // 🔁 LOOP STARTS HERE
    for (let item in bill) {
        let total = bill[item].qty * bill[item].price;
        subtotal += total;

        // ✅ THIS IS INSIDE FOR LOOP
        table.innerHTML += `
        <tr>
            <td>${item}</td>
            <td>
                <button onclick="changeQty('${item}', -1)">-</button>
                ${bill[item].qty}
                <button onclick="changeQty('${item}', 1)">+</button>
            </td>
            <td>₹${bill[item].price}</td>
            <td>₹${total}</td>
        </tr>
        `;
    }
    // 🔁 LOOP ENDS HERE
    
    gstEnabled = document.getElementById("gstToggle").checked;
    let gst = gstEnabled ? subtotal * 0.05 : 0;
    document.getElementById("subtotal").innerText = subtotal.toFixed(2);
    document.getElementById("gst").innerText = gst.toFixed(2);
    document.getElementById("total").innerText = (subtotal + gst).toFixed(2);
}*/

function changeQty(name, delta) {
    if (!bill[name]) return;

    bill[name].qty += delta;

    // ❌ do NOT allow qty < 1
    if (bill[name].qty < 1) {
        bill[name].qty = 1;
    }

    updateBill();
}

function printBill() {
    let gstEnabled = document.getElementById("gstToggle").checked;
    fetch("/save-bill", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            bill_no: document.getElementById("billno").innerText,
            cart: bill,
            gst: gstEnabled,
            payment: document.getElementById("payment").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success")
        {
            let frame = document.getElementById("printFrame");
            frame.src = "/print-bill/" + data.bill_no;
            bill = {};
            updateBill();
            alert("bill printed successfully");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error saving bill");
    });
}


/*function printBill() {
    console.log("print bill clicked");
    console.log(bill);
    alert("Bill printed successfully");

    let gstEnabled = document.getElementById("gstToggle").checked;

    fetch('/save-bill', {   // correct route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cart: bill,              
            gst: gstEnabled,        
            payment: document.getElementById('payment').value
        })
    })
    .then(res => res.json())
    .then(data => {
        // show bill no & date
        document.getElementById("billno").innerText = data.bill_no;
        document.getElementById("billdate").innerText = data.date;

        // clear bill
        bill = {};
        updateBill();
    })
    .catch(err => {
        console.error(err);
        alert("Error saving bill");
    });
}*/



/*function printBill() {
    console.log("print bill clicked");
    console.log(bill);
    alert("Bill printed successfully");

    fetch('/save-bill', {   // ✅ correct route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cart: bill,              // ✅ matches backend
            gst: gstEnabled,         // ✅ boolean true / false
            payment: document.getElementById('payment').value
        })
    })
    .then(res => res.json())
    .then(data => {
        // ✅ show bill no & date
        document.getElementById("billno").innerText = data.bill_no;
        document.getElementById("billdate").innerText = data.date;

        // ✅ clear bill
        bill = {};
        updateBill();
    })
    .catch(err => {
        console.error(err);
        alert("Error saving bill");
    });
}*/


/*function printBill()
{
    alert("Bill printed successfully");
    fetch('/save_bill', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
            items:bill,subtotal:parseFloat(document.getElementById('subtotal').innerText),
            gst:parseFloat(document.getElementById('gst').innerText),
            total:parseFloat(document.getElementById('total').innerText),
            payment:document.getElementById('payment').value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("billNo").innerText = data.bill_no;
        document.getElementById("billdate").innerText = data.date;
    


        bill = {};
        updateBill();
    
    });
}


/*function updateBill()
{
    let table = document.getElementById("billtable");
    table.innerHTML = '
    <tr>
        <th>Item</th>
        <th>Qty</th>
        <th>Total</th>
    </tr>';

    let subtotal = 0;
    for (let item in bill)
    {
        let total = bill[item].qty * bill[item].price;
        subtotal += total;

        table.innerHTML += "
        <tr>
             <td>${item}</td>
             <td>
                 <button onclick = "changeQty('${item}',-1)">-</button>
                  ${bill[item].qty}
                  <button onclick = "changeQty('${item}',1)">+</button>
                  </td>

                 <td>₹${bill[item].price}</td>
                <td>₹${total}</td>
                </tr>";

    }
    let gst = subtotal * 0.05;
    document.getElementById("subtotal").innerText = subtotal;
    document.getElementById("gst").innerText = gst.toFixed(2);
    document.getElementById("total").innerText = (subtotal + gst).toFixed(2);
}

function changeQty(item, value)
{
    bill[item].qty += value;
    if (bill[item].qty <= 0)delete bill[item];
    updateBill();
}

function printBill()
{
    alert("Bill printed successfully");
}

function updateBill() {
    let table = document.getElementById("billTable");

    // table header (once)
    table.innerHTML = `
        <tr>
            <th>Item</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Total</th>
        </tr>
    `;

    let subtotal = 0;

    // 🔁 LOOP STARTS HERE
    for (let item in bill) {
        let total = bill[item].qty * bill[item].price;
        subtotal += total;

        // ✅ THIS IS INSIDE FOR LOOP
        table.innerHTML += `
        <tr>
            <td>${item}</td>
            <td>
                <button onclick="changeQty('${item}', -1)">−</button>
                ${bill[item].qty}
                <button onclick="changeQty('${item}', 1)">+</button>
            </td>
            <td>₹${bill[item].price}</td>
            <td>₹${total}</td>
        </tr>
        `;
    }
    // 🔁 LOOP ENDS HERE

    let gst = subtotal * 0.05;
    document.getElementById("subtotal").innerText = subtotal;
    document.getElementById("gst").innerText = gst.toFixed(2);
    document.getElementById("total").innerText = (subtotal + gst).toFixed(2);
}
*/