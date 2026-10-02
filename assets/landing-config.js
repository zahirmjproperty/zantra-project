/* Public configuration only. NEVER place client secrets, tokens or session data here.
 *
 * ZENTRA-id (verified identity service for the ZPG family):
 *   service  : https://id.zentrapropertygroup.com
 *   endpoint : GET /sso/authorize?client_id=<id>&redirect_uri=<uri>&state=<state>
 *
 * HONEST STATUS: this host (project.zentrapropertygroup.com) is a STATIC GitHub Pages
 * site. No SSO client is registered for it and a static host cannot serve the
 * /sso/callback endpoint that exchanges the one-time code. Full sign-in therefore is
 * NOT wired end-to-end. loginUrl below is an ENTRY LINK to the verified identity
 * service only. Set loginUrl to '' to show the honest "not configured" dialog.
 */
window.ZENTRA_CONFIG = Object.freeze({
  loginUrl: 'https://id.zentrapropertygroup.com',
  xmeUrl: 'https://xme.project.zentrapropertygroup.com',
  budimanUrl: 'https://budiman.project.zentrapropertygroup.com'
});
