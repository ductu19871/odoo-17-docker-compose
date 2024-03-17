/** @odoo-module **/
import { browser } from "@web/core/browser/browser";
import {download} from "@web/core/network/download";
import {registry} from "@web/core/registry";

registry
    .category("ir.actions.report handlers")
    .add("aeroo_handler", async function (action, options, env) {
        if (action.report_type === "aeroo") {
        	return _triggerAerooDownload(action, options);
        } else if (action.report_type === "qweb-pdf-browser") {
        	return _triggerOpenPdfBrowser(action, options)
        }
        
        async function _triggerAerooDownload(action, options) {
            env.services.ui.block();
            try {
                await download({
                	url: "/web/report_aeroo",
                    data: {
                		report_id: action.id,
                        record_ids: JSON.stringify(action.context.active_ids),
                        context: JSON.stringify(env.services.user.context),
                    },
                });
            } finally {
                env.services.ui.unblock();
            }
            const onClose = options.onClose;
            if (action.close_on_report_download) {
                return doAction({ type: "ir.actions.act_window_close" }, { onClose });
            } else if (onClose) {
                onClose();
            }
        }
        
        function _getReportUrl(action, type) {
        	let url = `/report/${type}/${action.report_name}`;
            const actionContext = action.context || {};
            if (action.data && JSON.stringify(action.data) !== "{}") {
                const options = encodeURIComponent(JSON.stringify(action.data));
                const context = encodeURIComponent(JSON.stringify(actionContext));
                url += `?options=${options}&context=${context}`;
            } else {
                if (actionContext.active_ids) {
                    url += `/${actionContext.active_ids.join(",")}`;
                }
                if (type === "html") {
                    const context = encodeURIComponent(JSON.stringify(env.services.user.context));
                    url += `?context=${context}`;
                }
            }
            return url;
        }
        
        function _triggerOpenPdfBrowser(action, options) {
        	const url = _getReportUrl(action, 'pdf');
            env.services.ui.block();
            if (!window.open(url)) {
            	const msg = env._t(
		                "A popup window has been blocked. You may need to change your " +
		                    "browser settings to allow popup windows for this page."
		            );
		            env.services.notification.add(msg, {
		                sticky: true,
		                type: "warning",
		            });
            }
            env.services.ui.unblock();
            return options.onClose
            
        }
        
    });