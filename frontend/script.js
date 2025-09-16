document.addEventListener('DOMContentLoaded', () => {
    // --- Element References ---
    const pptxFileInput = document.getElementById('pptx-file');
    const jpgFileInput = document.getElementById('jpg-file');
    const pptxFilename = document.getElementById('pptx-filename');
    const jpgFilename = document.getElementById('jpg-filename');
    const voiceSelect = document.getElementById('voice-select');
    const generateBtn = document.getElementById('generate-btn');
    const inputSection = document.getElementById('input-section');
    const outputSection = document.getElementById('output-section');
    const avatarImage = document.getElementById('avatar-image');
    const scriptContent = document.getElementById('script-content');
    const statusText = document.getElementById('status-text');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const stopBtn = document.getElementById('stop-btn');
    const backBtn = document.getElementById('back-btn');
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');
    const previewVoiceBtn = document.getElementById('preview-voice-btn');

    // --- State Variables ---
    let voices = [];
    const synth = window.speechSynthesis;
    let isPaused = false;
    let presentationScript = []; // Array to hold the script for each slide
    let currentSlideIndex = 0; // To track playback

    // --- Backend API Configuration ---
    const backendUrl = 'http://localhost:5000/api/process';

    // --- Voice Loading ---
    async function populateVoiceList() {
        try {
            // Get voices from backend
            const response = await fetch('http://localhost:5000/api/voices');
            const data = await response.json();
            
            voiceSelect.innerHTML = '';
            const defaultOption = document.createElement('option');
            defaultOption.textContent = 'Select a narrator voice...';
            defaultOption.disabled = true;
            defaultOption.selected = true;
            voiceSelect.appendChild(defaultOption);
            
            if (data.voices && data.voices.length > 0) {
                data.voices.forEach(voice => {
                    const option = document.createElement('option');
                    option.textContent = `${voice.name} (${voice.language})`;
                    option.setAttribute('data-name', voice.name);
                    voiceSelect.appendChild(option);
                });
                // Enable preview button when voices are loaded
                previewVoiceBtn.disabled = false;
            } else {
                // Fallback to browser voices
                voices = synth.getVoices();
                if (voices.length > 0) {
                    voices.forEach(voice => {
                        const option = document.createElement('option');
                        option.textContent = `${voice.name} (${voice.lang})`;
                        option.setAttribute('data-name', voice.name);
                        voiceSelect.appendChild(option);
                    });
                } else {
                    voiceSelect.innerHTML = '<option>No voices available</option>';
                }
            }
        } catch (error) {
            console.error('Error loading voices:', error);
            voiceSelect.innerHTML = '<option>Error loading voices</option>';
        }
    }
    
    // Load voices when page loads
    populateVoiceList();

    // --- Voice Preview Functionality ---
    previewVoiceBtn.addEventListener('click', async () => {
        const selectedVoiceName = voiceSelect.options[voiceSelect.selectedIndex]?.getAttribute('data-name');
        
        if (!selectedVoiceName) {
            alert('Please select a voice first');
            return;
        }

        // Disable button and show loading
        previewVoiceBtn.disabled = true;
        previewVoiceBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span class="hidden sm:inline">Generating...</span>';

        try {
            const response = await fetch('http://localhost:5000/api/preview-voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    voice_name: selectedVoiceName
                })
            });

            const result = await response.json();

            if (result.success && result.download_url) {
                // Create audio element and play the preview
                const audio = new Audio(`http://localhost:5000${result.download_url}`);
                
                audio.onloadstart = () => {
                    previewVoiceBtn.innerHTML = '<i class="fas fa-volume-up"></i><span class="hidden sm:inline">Playing...</span>';
                };
                
                audio.onended = () => {
                    previewVoiceBtn.innerHTML = '<i class="fas fa-play"></i><span class="hidden sm:inline">Preview</span>';
                    previewVoiceBtn.disabled = false;
                };
                
                audio.onerror = () => {
                    throw new Error('Failed to play audio preview');
                };
                
                audio.play();
                
            } else {
                throw new Error(result.error || 'Failed to generate preview');
            }
        } catch (error) {
            console.error('Voice preview error:', error);
            alert('Failed to preview voice. Please try again.');
            previewVoiceBtn.innerHTML = '<i class="fas fa-play"></i><span class="hidden sm:inline">Preview</span>';
            previewVoiceBtn.disabled = false;
        }
    });

    // --- File Input Handlers ---
    pptxFileInput.addEventListener('change', () => {
        pptxFilename.textContent = pptxFileInput.files.length > 0 ? pptxFileInput.files[0].name : 'Drop a .pptx or .pdf file here or click';
    });
    jpgFileInput.addEventListener('change', () => {
        if (jpgFileInput.files.length > 0) {
            const file = jpgFileInput.files[0];
            jpgFilename.textContent = file.name;
            const reader = new FileReader();
            reader.onload = (e) => avatarImage.src = e.target.result;
            reader.readAsDataURL(file);
        } else {
            jpgFilename.textContent = 'Drop an image file here or click';
            avatarImage.src = 'https://placehold.co/256x256/1e1b4b/93c5fd?text=Avatar';
        }
    });

    // --- Core Logic: Generate Button Click ---
    generateBtn.addEventListener('click', async () => {
        if (!pptxFileInput.files[0] || !jpgFileInput.files[0]) {
            alert("Please upload both a presentation and an avatar image.");
            return;
        }

        // --- Switch to Output View ---
        inputSection.style.opacity = 0;
        setTimeout(() => {
            inputSection.classList.add('hidden');
            outputSection.classList.remove('hidden');
            outputSection.style.opacity = 1;
        }, 500);

        statusText.textContent = 'Uploading and processing presentation...';
        playPauseBtn.disabled = true;
        stopBtn.disabled = true;

        const formData = new FormData();
        formData.append('pptx_file', pptxFileInput.files[0]);
        formData.append('face_file', jpgFileInput.files[0]);
        
        // Add selected voice information
        const selectedVoiceName = voiceSelect.options[voiceSelect.selectedIndex]?.getAttribute('data-name');
        if (selectedVoiceName) {
            formData.append('selected_voice', selectedVoiceName);
        }

        try {
            // 1. Send files to backend and get the script
            const response = await fetch(backendUrl, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to process presentation.');
            }

            // --- Safe handling of backend response ---
            if (Array.isArray(result.slides)) {
                presentationScript = result.slides.map(s => s.narration || "");
            } else if (Array.isArray(result.script)) {
                presentationScript = result.script;
            } else {
                presentationScript = [];
                statusText.textContent = 'Invalid server response: presentation script missing.';
                console.error('Unexpected backend response:', result);
                return; // Stop further processing
            }

            // 2. Display script and start monitoring progress
            displayScript();
            statusText.textContent = 'Processing video...';
            
            // Start polling for status updates
            pollProcessingStatus();

        } catch (error) {
            console.error("Error during presentation generation:", error);
            statusText.textContent = `An error occurred: ${error.message}`;
        }
    });

    // --- UI and Playback Functions ---
    function displayScript() {
        scriptContent.innerHTML = '';
        presentationScript.forEach((text, index) => {
            const slideContainer = document.createElement('div');
            slideContainer.id = `slide-container-${index}`;
            slideContainer.className = 'p-3 my-2 rounded-lg transition-colors duration-300';

            const title = document.createElement('h4');
            title.className = 'font-bold text-indigo-100 mb-1';
            title.textContent = `Slide ${index + 1}`;

            const p = document.createElement('p');
            p.textContent = text;

            slideContainer.appendChild(title);
            slideContainer.appendChild(p);
            scriptContent.appendChild(slideContainer);
        });
    }

    function playSlide(slideIndex) {
        if (slideIndex >= presentationScript.length || synth.speaking) {
            if (slideIndex >= presentationScript.length) {
                // End of presentation
                avatarImage.classList.remove('speaking');
                statusText.textContent = 'Presentation Finished!';
                playIcon.classList.remove('hidden');
                pauseIcon.classList.add('hidden');
                currentSlideIndex = 0; // Reset for replay
            }
            return;
        }

        isPaused = false;
        const textToSpeak = presentationScript[slideIndex];
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        const selectedVoiceName = voiceSelect.options[voiceSelect.selectedIndex]?.getAttribute('data-name');
        const selectedVoice = voices.find(v => v.name === selectedVoiceName);
        if (selectedVoice) utterance.voice = selectedVoice;

        utterance.onstart = () => {
            avatarImage.classList.add('speaking');
            statusText.textContent = `Playing Slide ${slideIndex + 1}...`;
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');

            document.querySelectorAll('[id^="slide-container-"]').forEach(el => el.classList.remove('bg-indigo-500/50'));
            const currentSlideEl = document.getElementById(`slide-container-${slideIndex}`);
            currentSlideEl.classList.add('bg-indigo-500/50');
            currentSlideEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        };

        utterance.onend = () => {
            currentSlideIndex++;
            playSlide(currentSlideIndex); // Automatically play the next slide
        };

        utterance.onerror = (e) => console.error('SpeechSynthesis Error', e);

        synth.speak(utterance);
    }

    // --- Media Controls ---
    playPauseBtn.addEventListener('click', () => {
        if (synth.speaking && !isPaused) {
            synth.pause();
            isPaused = true;
            avatarImage.classList.remove('speaking');
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
            statusText.textContent = `Paused on Slide ${currentSlideIndex + 1}`;
        } else if (isPaused) {
            synth.resume();
            isPaused = false;
            avatarImage.classList.add('speaking');
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
            statusText.textContent = `Playing Slide ${currentSlideIndex + 1}...`;
        } else {
            playSlide(currentSlideIndex);
        }
    });

    stopBtn.addEventListener('click', () => {
        synth.cancel();
        avatarImage.classList.remove('speaking');
        statusText.textContent = 'Presentation Stopped.';
        currentSlideIndex = 0;
        isPaused = false;
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
        document.querySelectorAll('[id^="slide-container-"]').forEach(el => el.classList.remove('bg-indigo-500/50'));
    });

    backBtn.addEventListener('click', () => {
        synth.cancel();
        outputSection.style.opacity = 0;
        setTimeout(() => {
            outputSection.classList.add('hidden');
            inputSection.classList.remove('hidden');
            inputSection.style.opacity = 1;
        }, 500);

        // --- Reset State and UI ---
        pptxFileInput.value = '';
        jpgFileInput.value = '';
        pptxFilename.textContent = 'Drop a .pptx or .pdf file here or click';
        jpgFilename.textContent = 'Drop an image file here or click';
        avatarImage.src = 'https://placehold.co/256x256/1e1b4b/93c5fd?text=Avatar';
        scriptContent.innerHTML = '<p class="text-gray-400">Presentation script will appear here...</p>';
        presentationScript = [];
        currentSlideIndex = 0;
        playPauseBtn.disabled = true;
        stopBtn.disabled = true;
        previewVoiceBtn.disabled = false;
        previewVoiceBtn.innerHTML = '<i class="fas fa-play"></i><span class="hidden sm:inline">Preview</span>';
        isPaused = false;
    });

    // --- Status Polling Function ---
    function pollProcessingStatus() {
        const statusInterval = setInterval(async () => {
            try {
                const response = await fetch('http://localhost:5000/api/status');
                const status = await response.json();
                
                if (status.status === 'completed') {
                    clearInterval(statusInterval);
                    statusText.textContent = 'Video ready! Click play to start presentation.';
                    playPauseBtn.disabled = false;
                    stopBtn.disabled = false;
                    
                    // Add download button
                    addDownloadButton();
                } else if (status.status === 'error') {
                    clearInterval(statusInterval);
                    statusText.textContent = `Error: ${status.error}`;
                    playPauseBtn.disabled = true;
                    stopBtn.disabled = true;
                } else if (status.status === 'processing') {
                    statusText.textContent = `${status.current_step} (${status.progress}%)`;
                }
            } catch (error) {
                console.error('Error polling status:', error);
            }
        }, 2000); // Poll every 2 seconds
    }

    // --- Add Download Button ---
    function addDownloadButton() {
        const downloadBtn = document.createElement('button');
        downloadBtn.innerHTML = '<i class="fas fa-download mr-2"></i>Download Video';
        downloadBtn.className = 'generate-button mt-4';
        downloadBtn.onclick = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/download');
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'final_presentation_with_slides.mp4';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                } else {
                    alert('Video not ready yet. Please wait for processing to complete.');
                }
            } catch (error) {
                console.error('Download error:', error);
                alert('Error downloading video. Please try again.');
            }
        };
        
        // Add download button after the back button
        const backButtonContainer = backBtn.parentElement;
        backButtonContainer.appendChild(downloadBtn);
    }
});
