import streamlit as st

# Set page config
st.set_page_config(page_title="NextHop AI", layout="wide")

# Inject Tailwind CSS via CDN
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');
    </style>
""", unsafe_allow_html=True)

# Custom HTML
st.markdown("""
<div class="bg-gray-50 min-h-screen font-sans">

    <!-- Header -->
    <header class="flex justify-between items-center p-6 max-w-7xl mx-auto">
        <div class="flex items-center gap-2">
            <img src="https://via.placeholder.com/25x25" alt="Logo" class="h-6 w-6">
            <span class="font-bold text-lg">NextHop AI</span>
        </div>
        <nav class="space-x-8 text-gray-800 font-medium">
            <a href="#">Home</a>
            <a href="#">Tools</a>
            <a href="#">Pricing</a>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="flex flex-col lg:flex-row items-center justify-between max-w-7xl mx-auto p-6 lg:py-16">
        <!-- Text -->
        <div class="max-w-xl">
            <h1 class="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
                <span class="text-pink-600">NextHop AI</span> – Your AI Assistant for Network Engineering
            </h1>
            <p class="text-gray-700 text-lg mb-6">
                Analyze, generate, and streamline configurations with AI-powered tools built for modern network engineers.
            </p>
            <a href="#" class="inline-block px-6 py-3 bg-white border border-gray-300 rounded-lg shadow hover:shadow-md transition text-gray-900 font-medium">
                Try Now →
            </a>
        </div>

        <!-- Image -->
        <div class="mt-10 lg:mt-0 lg:ml-16">
            <div class="rounded-2xl overflow-hidden shadow-lg border border-gray-200">
                <img src="https://images.unsplash.com/photo-1556742044-3c52d6e88c62" alt="AI Engineer" class="w-[500px] h-[320px] object-cover">
            </div>
        </div>
    </section>

</div>
""", unsafe_allow_html=True)
