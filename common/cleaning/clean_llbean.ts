const { readFile, writeFile } = require('fs').promises;
const argv = require('yargs').argv;

const inputFileName = argv._[0];
const outputFileName = argv._[1];

const parseJSONFile = async (fileName: String) => {
  try {
    const file = await readFile(fileName);
    return JSON.parse(file);
  } catch (err) {
    console.log(err);
    process.exit(1);
  }
};

type ParseResponse = {
  [key: string]: any;
};

const flattenObject = (obj: Object): ParseResponse => {
  let flattenKeys = {};
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

// const arrayToCSV = (data) => {
//   // console.log(data[0]);
//   const csvt = flattenObject(data);
//   console.log(csvt);
//   let csv = csvt.foreach((row) => Object.keys(row));
//   csv.unshift(Object.keys(data));
//   return `${csv.join('\n')}`;
// };

const arrayCSV = (data: Object) => {
  let csv = flattenObject(data);

  const header = csv.map((row) => {
    Object.keys(row.split('.', 1));
  });

  csv += header;
  console.log(csv);

  return csv;
};

const writeCSV = async (fileName: String, data: Object) => {
  try {
    await writeFile(fileName, data, 'utf8');
  } catch (err) {
    console.log(err);
    process.exit(1);
  }
};

(async () => {
  const data = await parseJSONFile(inputFileName);
  const CSV = arrayCSV(data);
  await writeCSV(outputFileName, CSV);
  console.log(`Successfully converted ${outputFileName}!`);
})();
