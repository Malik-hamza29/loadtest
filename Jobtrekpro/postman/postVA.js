// --- Random First Name ---
const firstNames = ["John", "Emily", "Lucas", "Sofia", "Daniel", "Ava", "Michael"];
let first = firstNames[Math.floor(Math.random() * firstNames.length)];
pm.collectionVariables.set("first", first);

// --- Random Last Name ---
const lastNames = ["Smith", "Johnson", "Brown", "Taylor", "Williams", "Davis", "Miller"];
let last = lastNames[Math.floor(Math.random() * lastNames.length)];
pm.collectionVariables.set("last", last);

// --- RANDOM YOPMAIL EMAIL ---
let yop = `${first.toLowerCase()}.${last.toLowerCase()}${Math.floor(Math.random() * 1000)}@yopmail.com`;
pm.collectionVariables.set("email", yop);

// --- Random Phone Number ---
pm.collectionVariables.set(
    "mobile_number",
    `+1 (800) ${Math.floor(1000000 + Math.random() * 9000000)}`
);

console.log("Generated:", pm.collectionVariables.toObject());
