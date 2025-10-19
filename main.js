// Startup Surakshate - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Auth modal functionality
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const authModal = document.getElementById('authModal');
    const closeAuthModal = document.getElementById('closeAuthModal');
    const authModalTitle = document.getElementById('authModalTitle');
    const authSwitchBtn = document.getElementById('authSwitchBtn');
    const authSwitchText = document.getElementById('authSwitchText');
    const submitAuthBtn = document.getElementById('submitAuthBtn');
    
    // Check if user is logged in
    checkAuthStatus();

    // Open login modal
    if (loginBtn && authModal) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openAuthModal('login');
        });
    }

    // Open signup modal
    if (signupBtn && authModal) {
        signupBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openAuthModal('signup');
        });
    }

    // Close auth modal
    if (closeAuthModal && authModal) {
        closeAuthModal.addEventListener('click', function() {
            authModal.classList.add('hidden');
        });
    }

    // Switch between login and signup
    if (authSwitchBtn) {
        authSwitchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const currentMode = authModalTitle.textContent.toLowerCase();
            if (currentMode === 'login') {
                openAuthModal('signup');
            } else {
                openAuthModal('login');
            }
        });
    }

    // Submit auth form
    if (submitAuthBtn) {
        submitAuthBtn.addEventListener('click', function() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const mode = authModalTitle.textContent.toLowerCase();
            
            if (!email || !password) {
                showToast('Please fill in all fields', 'error');
                return;
            }
            
            if (mode === 'login') {
                login(email, password);
            } else {
                signup(email, password);
            }
        });
    }

    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            logout();
        });
    }

    // Function to open auth modal
    function openAuthModal(mode) {
        if (mode === 'login') {
            authModalTitle.textContent = 'Login';
            submitAuthBtn.textContent = 'Login';
            authSwitchText.textContent = "Don't have an account?";
            authSwitchBtn.textContent = 'Sign up';
        } else {
            authModalTitle.textContent = 'Sign Up';
            submitAuthBtn.textContent = 'Sign Up';
            authSwitchText.textContent = 'Already have an account?';
            authSwitchBtn.textContent = 'Login';
        }
        authModal.classList.remove('hidden');
    }

    // Function to check auth status
    async function checkAuthStatus() {
        try {
            const response = await fetch('/api/auth/me', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.user) {
                    // User is logged in
                    showUserMenu(data.user.email);
                } else {
                    // User is not logged in
                    showGuestMenu();
                }
            } else {
                // Error or not logged in
                showGuestMenu();
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
            showGuestMenu();
        }
    }

    // Function to login
    async function login(email, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            if (response.ok) {
                const data = await response.json();
                showToast('Login successful!', 'success');
                authModal.classList.add('hidden');
                showUserMenu(email);
                
                // Redirect to dashboard after login
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                const error = await response.json();
                showToast(error.detail || 'Login failed. Please check your credentials.', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            showToast('An error occurred during login. Please try again.', 'error');
        }
    }

    // Function to signup
    async function signup(email, password) {
        try {
            const response = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            if (response.ok) {
                const data = await response.json();
                showToast('Account created successfully!', 'success');
                authModal.classList.add('hidden');
                showUserMenu(email);
                
                // Redirect to dashboard after signup
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                const error = await response.json();
                showToast(error.detail || 'Signup failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Signup error:', error);
            showToast('An error occurred during signup. Please try again.', 'error');
        }
    }

    // Function to logout
    async function logout() {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                showToast('Logged out successfully!', 'success');
                showGuestMenu();
                
                // Redirect to home page after logout
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showToast('Logout failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Logout error:', error);
            showToast('An error occurred during logout. Please try again.', 'error');
        }
    }

    // Function to show user menu
    function showUserMenu(email) {
        const userMenu = document.getElementById('userMenu');
        const guestMenu = document.getElementById('guestMenu');
        const userName = document.getElementById('userName');
        
        if (userMenu && guestMenu && userName) {
            userName.textContent = email;
            userMenu.classList.remove('hidden');
            guestMenu.classList.add('hidden');
        }
    }

    // Function to show guest menu
    function showGuestMenu() {
        const userMenu = document.getElementById('userMenu');
        const guestMenu = document.getElementById('guestMenu');
        
        if (userMenu && guestMenu) {
            userMenu.classList.add('hidden');
            guestMenu.classList.remove('hidden');
        }
    }

    // Function to show toast notification
    function showToast(message, type = 'info') {
        // Check if a toast already exists and remove it
        const existingToast = document.querySelector('.toast');
        if (existingToast) {
            existingToast.remove();
        }
        
        // Create new toast
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="flex items-center">
                <div class="mr-2">
                    ${type === 'success' ? '<i class="fas fa-check-circle text-green-500"></i>' : ''}
                    ${type === 'error' ? '<i class="fas fa-exclamation-circle text-red-500"></i>' : ''}
                    ${type === 'info' ? '<i class="fas fa-info-circle text-blue-500"></i>' : ''}
                </div>
                <div>${message}</div>
                <button class="ml-4 text-gray-400 hover:text-gray-600" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);
        
        // Hide toast after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 5000);
    }

    // Demo mode for hackathon
    // This allows the app to work without actual backend functionality
    window.demoMode = {
        isLoggedIn: false,
        login: function(email) {
            this.isLoggedIn = true;
            showUserMenu(email);
            showToast('Demo login successful!', 'success');
            
            // Store in session storage for demo
            sessionStorage.setItem('demoUser', email);
            
            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        },
        logout: function() {
            this.isLoggedIn = false;
            showGuestMenu();
            showToast('Demo logout successful!', 'success');
            
            // Clear from session storage
            sessionStorage.removeItem('demoUser');
            
            // Redirect to home
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
        },
        checkStatus: function() {
            const demoUser = sessionStorage.getItem('demoUser');
            if (demoUser) {
                this.isLoggedIn = true;
                showUserMenu(demoUser);
            } else {
                this.isLoggedIn = false;
                showGuestMenu();
            }
        }
    };
    
    // Initialize demo mode
    window.demoMode.checkStatus();
    
    // Override auth functions for demo mode
    if (submitAuthBtn) {
        submitAuthBtn.addEventListener('click', function() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                showToast('Please fill in all fields', 'error');
                return;
            }
            
            // Demo login
            window.demoMode.login(email);
            authModal.classList.add('hidden');
        });
    }
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            window.demoMode.logout();
        });
    }
});