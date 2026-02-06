/**
 * Conversation storage utility for persisting conversation_id in localStorage.
 *
 * Implements conversation persistence requirement for stateless server design.
 */

const CONVERSATION_ID_KEY = 'ai_chatbot_conversation_id';

export const conversationStorage = {
  /**
   * Get conversation ID from localStorage.
   *
   * @returns Conversation ID or null if not found
   */
  getConversationId(): number | null {
    if (typeof window === 'undefined') return null;

    const stored = localStorage.getItem(CONVERSATION_ID_KEY);
    if (!stored) return null;

    const conversationId = parseInt(stored, 10);
    return isNaN(conversationId) ? null : conversationId;
  },

  /**
   * Save conversation ID to localStorage.
   *
   * @param conversationId - Conversation ID to store
   */
  setConversationId(conversationId: number): void {
    if (typeof window === 'undefined') return;

    localStorage.setItem(CONVERSATION_ID_KEY, conversationId.toString());
  },

  /**
   * Clear conversation ID from localStorage (start new conversation).
   */
  clearConversationId(): void {
    if (typeof window === 'undefined') return;

    localStorage.removeItem(CONVERSATION_ID_KEY);
  },

  /**
   * Check if conversation ID exists in localStorage.
   *
   * @returns True if conversation ID exists
   */
  hasConversationId(): boolean {
    return this.getConversationId() !== null;
  }
};
