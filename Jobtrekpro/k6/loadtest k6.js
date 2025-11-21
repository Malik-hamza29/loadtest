import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {

    stages: [
        { duration: '10s', target: 5 },
        { duration: '5s', target: 10 },
        { duration: '3s', target: 25 },
        { duration: '3s', target: 50 },
    ],
}


// Login once before all VUs
export function setup() {
    const loginRes = http.post(
        'https://api.jobtrekpro.com/api/auth/login',
        JSON.stringify({ email: 'manualtesting@yopmail.com', password: 'Orange@12' }),
        { headers: { 'Content-Type': 'application/json' } }
    );
    check(loginRes, { 'login successful': (r) => r.status === 200 });
    const body = loginRes.json();
    const token = body.access_token || body.token || body.data?.access_token || body.data?.token;
    if (!token) throw new Error(`Token not found: ${loginRes.body}`);
    return { token };
}
// Load test scenarios for each VU
export default function (data) {
    const headers = { Authorization: `Bearer ${data.token}` };
    // Test dashboard
    const dashboardRes = http.get('https://stagingapp.jobtrekpro.com/dashboard/contractors', { headers });
    check(dashboardRes, { 'dashboard status 200': (r) => r.status === 200 });
    sleep(1);
    // Add more endpoints as needed
    const apiRes = http.get('https://api.jobtrekpro.com/api/clients', { headers });
    check(apiRes, { 'clients api status 200': (r) => r.status === 200 });

    const jobRes = http.get('https://api.jobtrekpro.com/api/jobs', { headers });
    check(apiRes, { 'jobs api status 200': (r) => r.status === 200 });

    const contractorRes = http.get('https://api.jobtrekpro.com/api/contractors', { headers });
    check(contractorRes, { 'contractors api status 200': (r) => r.status === 200 });

    const chatRes = http.get('https://api.jobtrekpro.com/api/chats', { headers });
    check(chatRes, { 'chats api status 200': (r) => r.status === 200 });



    // Add more endpoints as needed
    // const apiRes = http.get('https://api.jobtrekpro.com/api/endpoint', { headers });
    // check(apiRes, { 'api status 200': (r) => r.status === 200 });
}










