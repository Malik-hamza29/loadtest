const firstNames = ["John", "Emily", "Lucas", "Sofia", "Daniel", "Ava", "Michael"];
const lastNames = ["Smith", "Johnson", "Brown", "Taylor", "Williams", "Davis", "Miller"];
const addresses = [
    "742 Evergreen Terrace",
    "1313 Mockingbird Lane",
    "221B Baker Street",
    "1600 Pennsylvania Ave",
    "12 Grimmauld Place"
];
const tags = ["vip", "new", "returning", "premium", "test"];
const colors = ["red", "blue", "green", "yellow", "purple"];

// Generate random data
let first = firstNames[Math.floor(Math.random() * firstNames.length)];
let last = lastNames[Math.floor(Math.random() * lastNames.length)];

pm.collectionVariables.set("first", first);
pm.collectionVariables.set("last", last);
pm.collectionVariables.set("email", `${first.toLowerCase()}.${last.toLowerCase()}@example.com`);
pm.collectionVariables.set("phone", `+1 (800) ${Math.floor(1000000 + Math.random() * 9000000)}`);
pm.collectionVariables.set("address", addresses[Math.floor(Math.random() * addresses.length)]);
pm.collectionVariables.set("selected_tag", tags[Math.floor(Math.random() * tags.length)]);
pm.collectionVariables.set("selected_color", colors[Math.floor(Math.random() * colors.length)]);

console.log("Generated Variables:", pm.collectionVariables.toObject());
