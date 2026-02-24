/**
 * API service for KYNEĒ Console
 */

import axios from 'axios';
import { Agent, Finding, Engagement } from '../types';

const API_BASE_URL = '/api/v1';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Agents
  agents: {
    list: () => client.get<Agent[]>('/agents'),
    get: (agentId: string) => client.get<Agent>(`/agents/${agentId}`),
    enroll: (agentId: string) => client.post('/agents/enroll', { agent_id: agentId }),
  },

  // Findings
  findings: {
    list: (engagementId?: string) =>
      client.get<Finding[]>('/findings', {
        params: engagementId ? { engagement_id: engagementId } : {},
      }),
    get: (findingId: string) => client.get<Finding>(`/findings/${findingId}`),
    create: (finding: Partial<Finding>) => client.post('/findings', finding),
  },

  // Engagements
  engagements: {
    list: () => client.get<Engagement[]>('/engagements'),
    get: (engagementId: string) => client.get<Engagement>(`/engagements/${engagementId}`),
    create: (engagement: Partial<Engagement>) =>
      client.post('/engagements', engagement),
  },

  // Health check
  health: () => client.get('/health'),
};

export default api;
