import { defineStore } from 'pinia';
import axios from 'axios';

export const useSummaryStore = defineStore('summary', {
  state: () => ({
    ocr_completed: 0,
    ocr_pending: 0,
    ocr_records: []
  }),

  actions: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://localhost:5000/summary');
        this.ocr_completed = response.data.ocr_completed;
        this.ocr_pending = response.data.ocr_pending;
        this.ocr_records = response.data.ocr_records;
      } catch (error) {
        console.error('Error fetching summary data:', error);
      }
    },
    getRecordById(id) {
      return this.ocr_records.find(obj => obj.id == Number(id));
    }
  }
});
