export function abbrRoundNumber(num, digits=1) {
  const si = [
    { value: 1E9,  symbol: "G" },
    { value: 1E6,  symbol: "M" },
    { value: 1E3,  symbol: "k" }
  ];
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value).toFixed(digits)
        .replace(/\.0+$|(\.[0-9]*[1-9])0+$/, "$1") + si[i].symbol;
    }
  }
  return num.toString();
}
