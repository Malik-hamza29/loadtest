// Random utility functions
function randomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomDateOfBirth() {
    const age = randomInt(21, 65);
    const today = new Date();
    const birthYear = today.getFullYear() - age;
    const birthMonth = randomInt(0, 11);
    const birthDay = randomInt(1, 28);
    return `${birthYear}-${String(birthMonth + 1).padStart(2, '0')}-${String(birthDay).padStart(2, '0')}`;
}

// Pools
const firstNames = ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Sarah', 'Jennifer', 'Lisa', 'Mary'];
const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'];
const tags = ["urgent", "vip", "priority", "certified", "active"];
const tagColors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
const specializations = ["electrical", "plumbing", "hvac", "carpentry", "painting"];
const skillLevels = ["beginner", "intermediate", "advanced", "expert"];
const vehicleTypes = ["car", "truck", "van", "suv"];
const addresses = ["123 Main Street", "456 Oak Avenue", "789 Elm Boulevard", "321 Pine Road"];

// Generate random contractor
const firstName = randomChoice(firstNames);
const lastName = randomChoice(lastNames);
const hasVehicle = Math.random() < 0.5;

const payload = {
    firstName,
    lastName,
    email: `cont${Date.now()}@yopmail.com`, // unique email
    phone: `+1 (${randomInt(100, 999)}) ${randomInt(1000000, 9999999)}`,
    dateOfBirth: randomDateOfBirth(),
    homeBaseAddress: randomChoice(addresses),
    serviceRadius: randomChoice([10, 15, 25, 30, 50]),
    hourlyRate: randomInt(20, 100),
    yearsExperience: randomInt(1, 40),
    skillLevel: randomChoice(skillLevels),
    specializations: [randomChoice(specializations)],
    hasVehicle: hasVehicle,
    vehicleType: hasVehicle ? randomChoice(vehicleTypes) : null,
    ownsTools: Math.random() < 0.5,
    tags: [{ name: randomChoice(tags), color: randomChoice(tagColors) }],
    serviceAreas: [],
    licenseNumber: null,
    licenseState: null,
    insuranceProvider: null,
    emergencyContactName: null,
    emergencyContactPhone: null
};

// Save payload as Postman variable
pm.variables.set("contractorPayload", JSON.stringify(payload));
