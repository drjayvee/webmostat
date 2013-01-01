YUI.add('webmostat', function(Y) {
    function Webmostat(config) {
        Webmostat.superclass.constructor.apply(this, arguments);
    }
    Webmostat.NAME = 'webmostat';

    Y.Webmostat = Y.extend(Webmostat, Y.Base, {
        run: function () {
            new Y.TabView({srcNode: '#tabs'}).render();

            this._initControl();
            this._initTemperature();
            this._initSchedule();
        },

        _initControl: function () {
            Y.all('#control .yui3-button').each(function (input) {
                var pin = input.getAttribute('data-pin');

                new Y.ToggleButton({srcNode: input})
                    .render()
                    .after('pressedChange', function () {
                        this.set('label', this.get('disabled') ? 'Enable' : 'Disable');
                        Y.io( '/ajax/setThermostat', {
                            method: 'POST',
                            data: {
                                pin:        pin,
                                active:     Y.JSON.stringify(this.get('pressed'))
                            },
                            on: {
                                failure: function (ioId, res) {
                                    alert('Could not toggle thermostat: ' + res.responseText);
                                    this.set('disabled', true)
                                        .set('label', 'Broken!');
                                }
                            },
                            context: this
                        } );
                    });
            });
        },

        _initTemperature: function () {},

        _initSchedule: function () {}
    });
}, '0.1337', {requires: ['base', 'button', 'io', 'json-stringify', 'tabview']} );
