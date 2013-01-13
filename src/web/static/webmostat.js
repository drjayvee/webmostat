YUI.add('webmostat', function(Y) {
    function Webmostat(config) {
        Webmostat.superclass.constructor.apply(this, arguments);
    }
    Webmostat.NAME = 'webmostat';
    Webmostat.ATTRS = {
        tabView:   {},
        tempSeries: {
            writeOnce:  'initOnly'
        }
    };

    Y.extend(Webmostat, Y.Base, {
        run: function () {
            var tv = new Y.TabView({srcNode: '#tabs'});

            this.set('tabView', tv);
            tv.render();

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

        _initTemperature: function () {
            var chart,
                times = [],
                temps = [];

            this.get('tempSeries').forEach(function (temp){
                var time = new Date(temp[0] * 1000);

                times.push(time.getHours() + ':' + time.getMinutes());
                temps.push(temp[1]);
            });

            chart = new Y.Chart({
                dataProvider:   [times, temps],
                type:           'spline'
            });

            this.get('tabView').after('selectionChange', function (e) {
                if (e.newVal.get('index') === 1) {    // temps tab selected
                    chart.render( '#tempChart' );
                }
            });
        },

        _initSchedule: function () {}
    });

    Y.Webmostat = Webmostat;
}, '0.1337', {requires: ['base', 'button', 'charts', 'io', 'json-stringify', 'tabview']} );
