let bill = {};

function addItem(name, price)
{
    if (!bill[name]) bill[name] = { qty: 0, price: price};
    bill[name].qty++;
    updateBill();
}

function updateBill() {
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