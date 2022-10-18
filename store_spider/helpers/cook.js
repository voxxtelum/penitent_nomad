const cookieList = require('./cookies.json');

//console.log(cookieList);

cookies = {};

cookieList.forEach((item) => {
  // console.log(item.name);
  // console.log(item.value);
  let name = `'${item.name}'`;
  let value = item.value;
  newCookie = { [name]: value };
  cookies = { ...cookies, ...newCookie };

  console.log(`${name} : ${value}`);
});

console.log(cookies);
