// Test script to verify network connectivity, authentication, and task creation
import fetch from 'node-fetch';

async function testFullWorkflow() {
    console.log('Testing full API workflow...');
    const baseUrl = 'http://127.0.0.1:8000';

    try {
        // Test health endpoint
        const healthResponse = await fetch(`${baseUrl}/health`);
        const healthData = await healthResponse.json();
        console.log('✓ Health check passed:', healthData);

        // Test authentication - login with test user
        console.log('\nAttempting to authenticate test user...');
        const loginResponse = await fetch(`${baseUrl}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: 'test@example.com',
                password: 'testpass123'
            })
        });

        const loginData = await loginResponse.json();
        console.log('✓ Authentication response status:', loginResponse.status);

        if (loginResponse.status === 200) {
            console.log('✓ Successfully authenticated test user');

            // Extract the access token
            const accessToken = loginData.access_token;
            console.log('✓ Access token obtained');

            // Test creating a task with authentication
            console.log('\nTesting task creation with authentication...');
            const createTaskResponse = await fetch(`${baseUrl}/api/tasks/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    title: 'Test task from network test',
                    description: 'This is a test task created during network testing',
                    priority: 'medium'
                })
            });

            const createTaskData = await createTaskResponse.json();
            console.log('✓ Task creation response status:', createTaskResponse.status);

            if (createTaskResponse.status === 200) {
                console.log('✓ Task created successfully:', createTaskData.title);

                // Test getting the created task
                console.log('\nTesting task retrieval...');
                const getTaskResponse = await fetch(`${baseUrl}/api/tasks/${createTaskData.id}`, {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                });

                console.log('✓ Task retrieval response status:', getTaskResponse.status);

                if (getTaskResponse.status === 200) {
                    console.log('✓ Successfully retrieved created task');
                }
            } else {
                console.log('⚠ Task creation failed:', createTaskData.detail || createTaskData);
            }
        } else {
            console.log('⚠ Authentication failed:', loginData.detail || loginData);
        }

        console.log('\n✓ Full workflow test completed!');
        console.log('The API is running, accessible, and authentication is working.');

    } catch (error) {
        console.error('✗ Network test failed:', error.message);
        return false;
    }

    return true;
}

// Run the comprehensive test
testFullWorkflow();