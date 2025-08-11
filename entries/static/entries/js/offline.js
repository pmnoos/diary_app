// Offline form handling for diary entries
class OfflineEntryManager {
    constructor() {
        this.dbName = 'DiaryOfflineDB';
        this.version = 1;
        this.storeName = 'offlineEntries';
        this.init();
    }

    async init() {
        this.db = await this.openDB();
        this.setupFormHandlers();
        this.displayOfflineEntries();
    }

    openDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.version);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(this.storeName)) {
                    const store = db.createObjectStore(this.storeName, { keyPath: 'id', autoIncrement: true });
                    store.createIndex('timestamp', 'timestamp', { unique: false });
                    store.createIndex('synced', 'synced', { unique: false });
                }
            };
        });
    }

    async saveOfflineEntry(entryData) {
        const transaction = this.db.transaction([this.storeName], 'readwrite');
        const store = transaction.objectStore(this.storeName);
        
        const entry = {
            ...entryData,
            timestamp: Date.now(),
            synced: false
        };
        
        return store.add(entry);
    }

    async getOfflineEntries() {
        const transaction = this.db.transaction([this.storeName], 'readonly');
        const store = transaction.objectStore(this.storeName);
        
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    setupFormHandlers() {
        const forms = document.querySelectorAll('form[method="post"]');
        forms.forEach(form => {
            form.addEventListener('submit', async (e) => {
                if (!navigator.onLine) {
                    e.preventDefault();
                    await this.handleOfflineSubmission(form);
                }
            });
        });
    }

    async handleOfflineSubmission(form) {
        const formData = new FormData(form);
        const entryData = {
            title: formData.get('title'),
            date: formData.get('date'),
            content: formData.get('content'),
            is_private: formData.get('is_private') === 'on'
        };

        try {
            await this.saveOfflineEntry(entryData);
            this.showOfflineSuccessMessage();
            form.reset();
        } catch (error) {
            console.error('Failed to save offline entry:', error);
            this.showOfflineErrorMessage();
        }
    }

    showOfflineSuccessMessage() {
        const message = document.createElement('div');
        message.innerHTML = `
            <div style="background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0;">
                📱 Entry saved offline! It will sync when you're back online.
            </div>
        `;
        document.querySelector('main').prepend(message);
        
        setTimeout(() => message.remove(), 5000);
    }

    showOfflineErrorMessage() {
        const message = document.createElement('div');
        message.innerHTML = `
            <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0;">
                ❌ Failed to save entry offline. Please try again.
            </div>
        `;
        document.querySelector('main').prepend(message);
        
        setTimeout(() => message.remove(), 5000);
    }

    async displayOfflineEntries() {
        const entries = await this.getOfflineEntries();
        const unsynced = entries.filter(entry => !entry.synced);
        
        if (unsynced.length > 0 && document.querySelector('.entries-list')) {
            const banner = document.createElement('div');
            banner.innerHTML = `
                <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                    📱 You have ${unsynced.length} offline ${unsynced.length === 1 ? 'entry' : 'entries'} that will sync when you're back online.
                </div>
            `;
            document.querySelector('.entries-list').prepend(banner);
        }
    }

    async syncOfflineEntries() {
        if (!navigator.onLine) return;

        const entries = await this.getOfflineEntries();
        const unsynced = entries.filter(entry => !entry.synced);

        for (const entry of unsynced) {
            try {
                await this.syncEntry(entry);
                await this.markAsSynced(entry.id);
            } catch (error) {
                console.error('Failed to sync entry:', entry.id, error);
            }
        }
    }

    async syncEntry(entry) {
        const formData = new FormData();
        formData.append('title', entry.title);
        formData.append('date', entry.date);
        formData.append('content', entry.content);
        formData.append('is_private', entry.is_private);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        const response = await fetch('/entries/new/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Sync failed');
        }
    }

    async markAsSynced(entryId) {
        const transaction = this.db.transaction([this.storeName], 'readwrite');
        const store = transaction.objectStore(this.storeName);
        
        const entry = await store.get(entryId);
        entry.synced = true;
        await store.put(entry);
    }
}

// Initialize offline manager when page loads
document.addEventListener('DOMContentLoaded', () => {
    if ('indexedDB' in window) {
        window.offlineManager = new OfflineEntryManager();
    }
});

// Sync when coming back online
window.addEventListener('online', () => {
    if (window.offlineManager) {
        window.offlineManager.syncOfflineEntries();
    }
});
