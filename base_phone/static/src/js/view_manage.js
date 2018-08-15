odoo.define('tritam.view_manage', function(require) {
    "use strict";
    var config = require('web.config');
    var core = require('web.core');
    var data = require('web.data');
    var Model = require('web.DataModel');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var ViewManager = require('web.ViewManager');
    var _t = core._t;
    ViewManager.include({
        start: function() {
            var self = this;

            function IsJsonString(str) {
                try {
                    JSON.parse(str);
                } catch (e) {
                    return false;
                }
                return true;
            };
            this._super.apply(this, arguments);
            websocket.onmessage = function(e) {
                if (IsJsonString(e.data) == true) {
                    var obj = JSON.parse(e.data);
                    var url = window.location.href;
                    var argumens = url.indexOf("id");
                    var id = url.slice(argumens + 3, argumens + 4);
                    var toHHMMSS = (secs) => {
                        var sec_num = parseInt(secs, 10)
                        var hours = Math.floor(sec_num / 3600) % 24
                        var minutes = Math.floor(sec_num / 60) % 60
                        var seconds = sec_num % 60
                        return [hours, minutes, seconds]
                            .map(v => v < 10 ? "0" + v : v)
                            .filter((v, i) => v !== "00" || i > 0)
                            .join(":")
                    };
                    if (obj['action'] == 'incomingcall') {
                        var phone_no = obj['phonenumber'].toString()
                        var index = phone_no.indexOf("@")
                        self.do_action({
                            name: _t('Public Customer'),
                            type: 'ir.actions.act_window',
                            res_model: "res.partner",
                            views: [
                                [false, 'kanban'],
                                [false, 'form']
                            ],
                            domain: [
                                ['phone', '=', phone_no.substring(0, index)]
                            ],
                            target: 'new'
                        });
                    }
                    if (obj['action'] == 'callended' &&
                        url.search('form') != -1 && url.search('crm.lead') != -1) {
                                var date = new Date(obj['time_begin'])
                                var date_now = date.toString().substring(0, 25)
                                self.do_action({
                                    type: 'ir.actions.act_window',
                                    res_model: 'crm.activity.log',
                                    view_mode: 'form',
                                    view_type: 'form',
                                    views: [
                                        [false, 'form']
                                    ],
                                    context: {
                                        default_lead_id: parseInt(id),
                                        default_time_begin: date_now,
                                        default_duration: toHHMMSS(obj['duration']),
                                    },
                                    target: 'new'
                                })




                    }
                }
            };
        },
    });


});