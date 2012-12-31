YUI.add('webmostat', function(Y) {
    function Webmostat(config) {
        Webmostat.superclass.constructor.apply(this, arguments);
    }
    Webmostat.NAME = 'webmostat';
    Webmostat.ATTRS = {
        page: {
            value: 'none beeatch',
            writeOnce: 'initOnly'
        }
    };

    Y.Webmostat = Y.extend(Webmostat, Y.Base, {
        run: function () {
            var page = this.get('page' ),
                initFuncName = '_init' + page.charAt(0).toUpperCase() + page.slice(1);

            if ( !Y.Lang.isFunction(this[initFuncName]) ) {
                alert( 'Cannot init page' );
            }
            this[initFuncName]();
        },

        _initControl: function () {
            Y.all('.yui3-button').each(function (input) {
                var pin = input.getAttribute('data-pin');

                new Y.ToggleButton({srcNode: input})
                    .render()
                    .after('pressedChange', function () {
                        Y.io( '/ajax/setThermostat', {
                            method: 'POST',
                            data: {
                                pin:        pin,
                                active:     Y.JSON.stringify(this.get('pressed'))
                            },
                            on: {
                                success: function () {
                                  this.set('label', 'Disable');
                                },
                                failure: function (ioId, res) {
                                    alert('Could not toggle thermostat: ' + res.responseText);
                                    this.set('disabled', true)
                                        .set('label', 'Broken!');
                                }
                            },
                            context: this
                        } );
                    });
            } );
        },

        _initTemperature: function () {},

        _initSchedule: function () {}
    });
}, '0.1337', {requires: ['base', 'button', 'io', 'json-stringify']} );
