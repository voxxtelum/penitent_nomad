const { readFile, writeFile } = require('fs').promises;
const {
  Parser,
  transforms: { unwind },
} = require('json2csv');

const inputFileName = '../input/llbean_res.json';
const outputFileName = 'llbean_csv.csv';

const parseJSONFile = async (fileName) => {
  try {
    const file = await readFile(fileName);
    return JSON.parse(file);
  } catch (err) {
    console.log(err);
    process.exit(1);
  }
};

const flattenObject = (obj) => {
  let flattenKeys = [];
  for (let i in obj) {
    if (!obj.hasOwnProperty(i)) continue;
    if (typeof obj[i] == 'object') {
      // flattenKeys[i] = obj[i];
      let flatObject = flattenObject(obj[i]);
      for (let j in flatObject) {
        if (!flatObject.hasOwnProperty(j)) continue;
        flattenKeys[i + '.' + j] = flatObject[j];
      }
    } else {
      flattenKeys[i] = obj[i];
    }
  }
  return flattenKeys;
};

const jsonToCSV = (data) => {
  try {
    const fields = [
      'storeName',
      'shoppingCenter',
      'address.addressLine1',
      'address.city',
      'address.jurisdictionCode',
      'address.postalCode',
      'geoLocation.latitude',
      'geoLocation.longitude',
    ];
    const transforms = [unwind({ paths: ['address', 'geoLocation'] })];

    const jsonParser = new Parser({ fields, transforms });
    const csv = jsonParser.parse(data);

    // console.log(csv);

    return csv;
  } catch (err) {
    console.error(err);
  }
};

const writeCSV = async (fileName, data) => {
  try {
    await writeFile(fileName, data, 'utf8');
  } catch (err) {
    console.log(err);
    process.exit(1);
  }
};

(async () => {
  const data = await parseJSONFile(inputFileName);
  const csv = jsonToCSV(data);

  const o = JSON.stringify(csv);
  console.log(o);

  // console.log(csv);
  // const CSV = flatToCSV(data);
  await writeCSV(outputFileName, csv);
  console.log(`Successfully converted ${outputFileName}!`);
})();
