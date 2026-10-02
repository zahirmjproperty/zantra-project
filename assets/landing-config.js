/* Public configuration only. NEVER place client secrets, tokens or session data here.
 *
 * ZENTRA-id — the verified identity service shared by the ZPG systems:
 *   identity service : https://id.zentrapropertygroup.com
 *   authorize        : GET /sso/authorize?client_id=<id>&redirect_uri=<uri>&state=<state>
 *   token exchange   : POST /sso/token   (server-side only — never in static files)
 *   family route     : /sso/login on each system (sets state cookie, then redirects)
 *
 * HONEST STATUS — sign-in is NOT provisioned for this system:
 *   - no SSO client is registered for 'zentra-project' in the identity service
 *     (registered clients today: zentra-asset, zentra-value)
 *   - this host is a STATIC GitHub Pages site: it has no backend, so it cannot
 *     serve /sso/login or /sso/callback, and cannot perform the server-side
 *     code-to-identity exchange that requires the client secret.
 *
 * loginUrl is therefore set to the CORRECT family route (it will work unchanged
 * once the client is registered and a backend is provisioned) while
 * loginStatus='not-provisioned' makes the UI state the gap instead of pretending.
 * Set loginUrl to '' to fall back to the same honest dialog.
 */
window.ZENTRA_CONFIG = Object.freeze({
  loginUrl: '/sso/login',
  loginStatus: 'not-provisioned',
  identityUrl: 'https://id.zentrapropertygroup.com',
  xmeUrl: 'https://xme.project.zentrapropertygroup.com',
  budimanUrl: 'https://budiman.project.zentrapropertygroup.com'
});
