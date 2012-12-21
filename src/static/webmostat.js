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
				initFuncName = '_init' + page.charAt(0 ).toUpperCase() + page.slice(1);
			
			if ( !Y.Lang.isFunction(this[initFuncName]) ) {
				alert( 'Cannot init page' );
			}
			this[initFuncName]();
		},
		
		_initControl: function () {
			var liveButton = new Y.ToggleButton({srcNode: '#live'} ).render(),
				bathButton = new Y.ToggleButton({srcNode: '#bath'} ).render();
			
		},
		
		_initTemperature: function () {},
		
		_initSchedule: function () {}
	});
}, '0.1337', {requires: ['base', 'button', 'io', 'json-stringify']} );
