var resultArray = [document.getElementById("outputForStr"), document.getElementById("outputForNum")];

console.log(resultArray);

function displayResults() {

    resultArray.forEach((element) => {
        element.style.display = 'block';
    });

  const strA = document.getElementById("StringA").value;
  const strB = document.getElementById("StringB").value;
  document.getElementById('outputForStr').style.display = 'block';

  const strMethAndAns = [
    {
      desc: "Concatenation Operator",
      method: "strA + strB",
      output: strA + strB,
    },
    {
      desc: "String Length Method",
      method: "strA.length",
      output: strA.length,
    },
    {
      desc: "String to Upper Case Method",
      method: "strA.toUpperCase()",
      output: strA.toUpperCase(),
    },
    {
      desc: "String to Lower Case Method",
      method: "strA.toLowerCase()",
      output: strA.toLowerCase(),
    },
    {
      desc: "String Slice Method",
      method: "strA.slice(1, 3)",
      output: strA.slice(1, 3),
    },
    {
      desc: "String Substring Method",
      method: "strA.substring(1, 3)",
      output: strA.substring(1, 3),
    },
    {
      desc: "String Replace Method",
      method: "strA.replace('H', 'J')",
      output: strA.replace("H", "J"),
    },
    {
      desc: "String Char At Method",
      method: "strA.charAt(1)",
      output: strA.charAt(1),
    },
    {
      desc: "String Char Code At Method",
      method: "strA.charCodeAt(1)",
      output: strA.charCodeAt(1),
    },
    {
      desc: "String Index Of Method",
      method: "strA.indexOf('e')",
      output: strA.indexOf("e"),
    },
    {
      desc: "String Last Index Of Method",
      method: "strA.lastIndexOf('l')",
      output: strA.lastIndexOf("l"),
    },
    {
      desc: "String Search Method",
      method: "strA.search('ll')",
      output: strA.search("ll"),
    },
    {
      desc: "String Match Method",
      method: "strA.match(/l/g)",
      output: strA.match(/l/g),
    },
    {
      desc: "String Split Method",
      method: "strA.split('')",
      output: strA.split(""),
    },
    {
      desc: "String Trim Method",
      method: "strA.trim()",
      output: strA.trim(),
    },
    {
      desc: "String Value Of Method",
      method: "String(strA)",
      output: String(strA),
    },
    {
      desc: "String Locale Compare Method",
      method: "strA.localeCompare(strB)",
      output: strA.localeCompare(strB),
    },
    {
      desc: "String Repeat Method",
      method: "strA.repeat(2)",
      output: strA.repeat(2),
    },
    {
      desc: "String Includes Method",
      method: "strA.includes('ell')",
      output: strA.includes("ell"),
    },
    {
      desc: "String Starts With Method",
      method: "strA.startsWith('He')",
      output: strA.startsWith("He"),
    },
    {
      desc: "String Ends With Method",
      method: "strA.endsWith('lo')",
      output: strA.endsWith("lo"),
    },
    {
      desc: "String Pad Start Method",
      method: "strA.padStart(10, '*')",
      output: strA.padStart(10, "*"),
    },
    {
      desc: "String Pad End Method",
      method: "strA.padEnd(10, '*')",
      output: strA.padEnd(10, "*"),
    },
    {
      desc: "String Match All Method",
      method: "Array.from(strA.matchAll(/l/g))",
      output: Array.from(strA.matchAll(/l/g)),
    },
    {
      desc: "String Normalize Method",
      method: "strA.normalize()",
      output: strA.normalize(),
    },
    {
      desc: "String Code Point At Method",
      method: "strA.codePointAt(1)",
      output: strA.codePointAt(1),
    },
  ];

  const tableBody = document.getElementById("strTable");
  strMethAndAns.forEach((item) => {
    const row = document.createElement("tr");

    // Alternate row color beige and darker shade of beige
    if (tableBody.rows.length % 2 === 0) {
      row.style.backgroundColor = "#f5f5dc";
    } else {
      row.style.backgroundColor = "#f5f5af";
    }

    const descCell = document.createElement("td");
    descCell.textContent = item.desc;
    row.appendChild(descCell);

    const methodCell = document.createElement("td");
    methodCell.textContent = item.method;
    row.appendChild(methodCell);

    const outputCell = document.createElement("td");
    outputCell.textContent = Array.isArray(item.output)
      ? JSON.stringify(item.output)
      : item.output;
    row.appendChild(outputCell);

    strTable.appendChild(row);
  });
}

function displayResultsForNum() {
  resultArray.forEach((element) => {
    element.style.display = "block";
  });

  const numA = parseFloat(document.getElementById("NumberA").value);
  const numB = parseFloat(document.getElementById("NumberB").value);
  document.getElementById("outputForNum").style.display = "block";

  const numMethAndAns = [
    {
      desc: "Addition",
      method: "numA + numB",
      output: numA + numB,
    },
    {
      desc: "Subtraction",
      method: "numA - numB",
      output: numA - numB,
    },
    {
      desc: "Multiplication",
      method: "numA * numB",
      output: numA * numB,
    },
    {
      desc: "Division",
      method: "numA / numB",
      output: numB !== 0 ? numA / numB : "Division by zero error",
    },
    {
      desc: "Modulus",
      method: "numA % numB",
      output: numA % numB,
    },
    {
      desc: "Exponentiation",
      method: "Math.pow(numA, numB)",
      output: Math.pow(numA, numB),
    },
    {
      desc: "Square Root of numA",
      method: "Math.sqrt(numA)",
      output: Math.sqrt(numA),
    },
    {
      desc: "Round numA",
      method: "Math.round(numA)",
      output: Math.round(numA),
    },
    {
      desc: "Ceiling of numA",
      method: "Math.ceil(numA)",
      output: Math.ceil(numA),
    },
    {
      desc: "Floor of numA",
      method: "Math.floor(numA)",
      output: Math.floor(numA),
    },
    {
      desc: "Absolute value of numA",
      method: "Math.abs(numA)",
      output: Math.abs(numA),
    },
    {
      desc: "Max of numA and numB",
      method: "Math.max(numA, numB)",
      output: Math.max(numA, numB),
    },
    {
      desc: "Min of numA and numB",
      method: "Math.min(numA, numB)",
      output: Math.min(numA, numB),
    },
  ];

  // Fill number table
  const numTableBody = document.getElementById("numTable");
  numMethAndAns.forEach((item) => {
    const row = document.createElement("tr");

    // Alternate row color
    if (numTableBody.rows.length % 2 === 0) {
      row.style.backgroundColor = "#f5f5dc";
    } else {
      row.style.backgroundColor = "#f5f5af";
    }

    const descCell = document.createElement("td");
    descCell.textContent = item.desc;
    row.appendChild(descCell);

    const methodCell = document.createElement("td");
    methodCell.textContent = item.method;
    row.appendChild(methodCell);

    const outputCell = document.createElement("td");
    outputCell.textContent = Array.isArray(item.output)
      ? JSON.stringify(item.output)
      : item.output;
    row.appendChild(outputCell);

    numTableBody.appendChild(row);
  });
}