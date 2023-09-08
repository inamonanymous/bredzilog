function showPopUp(unique, name, address, phone, from_customer, referrenceNo, price, item) {
    var message = `
    Unique ID -> ${unique}
    Name -> ${name}
    Address -> ${address}
    Phone -> ${phone}
    From Customer -> ${from_customer}
    Reference No -> ${referrenceNo}
    Price -> ${price}
    Item -> ${item}
`;
alert(message);

}