import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(page_title="3-Month Step Challenge", page_icon="🏆", layout="wide")

# Initialize session state
if 'participants' not in st.session_state:
    st.session_state.participants = {
        'Riad': {'color': '#3B82F6', 'entries': []},
        'Keith': {'color': '#10B981', 'entries': []},
        'Hari': {'color': '#F59E0B', 'entries': []},
        'Victoria': {'color': '#EF4444', 'entries': []},
        'Leigeme': {'color': '#8B5CF6', 'entries': []},
        'Derek': {'color': '#EC4899', 'entries': []}
    }

# Load sample data on first run
if 'initialized' not in st.session_state:
    st.session_state.participants = {
        'Riad': {
            'color': '#3B82F6',
            'entries': [
                {'week_start': '2026-01-12', 'week_end': '2026-01-18', 'steps': 28000},
                {'week_start': '2026-01-19', 'week_end': '2026-01-25', 'steps': 32500},
                {'week_start': '2026-01-26', 'week_end': '2026-02-01', 'steps': 25000}
            ]
        },
        'Keith': {
            'color': '#10B981',
            'entries': [
                {'week_start': '2026-01-12', 'week_end': '2026-01-18', 'steps': 35000},
                {'week_start': '2026-01-19', 'week_end': '2026-01-25', 'steps': 42000},
                {'week_start': '2026-01-26', 'week_end': '2026-02-01', 'steps': 38000}
            ]
        },
        'Hari': {
            'color': '#F59E0B',
            'entries': [
                {'week_start': '2026-01-12', 'week_end': '2026-01-18', 'steps': 21000},
                {'week_start': '2026-01-19', 'week_end': '2026-01-25', 'steps': 24500},
                {'week_start': '2026-01-26', 'week_end': '2026-02-01', 'steps': 28000}
            ]
        },
        'Victoria': {
            'color': '#EF4444',
            'entries': [
                {'week_start': '2026-01-12', 'week_end': '2026-01-18', 'steps': 45000},
                {'week_start': '2026-01-19', 'week_end': '2026-01-25', 'steps': 52000},
                {'week_start': '2026-01-26', 'week_end': '2026-02-01', 'steps': 48000}
            ]
        },
        'Leigeme': {
            'color': '#8B5CF6',
            'entries': [
                {'week_start': '2026-01-12', 'week_end': '2026-01-18', 'steps': 18000},
                {'week_start': '2026-01-19', 'week_end': '2026-01-25', 'steps': 22000},
                {'week_start': '2026-01-26', 'week_end': '2026-02-01', 'steps': 19500}
            ]
        },
        'Derek': {
            'color': '#EC4899',
            'entries': [
                {'week_start': '2026-01-12', 'week_end': '2026-01-18', 'steps': 31000},
                {'week_start': '2026-01-19', 'week_end': '2026-01-25', 'steps': 29000},
                {'week_start': '2026-01-26', 'week_end': '2026-02-01', 'steps': 35000}
            ]
        }
    }
    st.session_state.initialized = True

def calculate_points(steps):
    """Calculate points based on step count"""
    points = steps // 100
    if steps >= 5000:
        points += 50
    if steps >= 7500:
        points += 75
    if steps >= 10000:
        points += 100
    if steps >= 12500:
        points += 150
    if steps >= 15000:
        points += 200
    return points

def get_participant_stats(name):
    """Get statistics for a participant"""
    entries = st.session_state.participants[name]['entries']
    if not entries:
        return {'total_steps': 0, 'total_points': 0, 'weeks': 0, 'avg_daily': 0}
    
    total_steps = sum(e['steps'] for e in entries)
    total_points = sum(calculate_points(e['steps']) for e in entries)
    weeks = len(entries)
    avg_daily = total_steps // (weeks * 7) if weeks > 0 else 0
    
    return {
        'total_steps': total_steps,
        'total_points': total_points,
        'weeks': weeks,
        'avg_daily': avg_daily
    }

def get_leaderboard():
    """Get leaderboard sorted by points"""
    leaderboard = []
    for name, data in st.session_state.participants.items():
        stats = get_participant_stats(name)
        leaderboard.append({
            'name': name,
            'color': data['color'],
            **stats
        })
    return sorted(leaderboard, key=lambda x: x['total_points'], reverse=True)

def get_distance_comparison(steps):
    """Convert steps to miles and provide real-world comparison"""
    # Average: 2,000 steps = 1 mile
    miles = steps / 2000
    km = miles * 1.609
    
    comparisons = [
       
        (2,   "🚶 Walking around Queen’s Park Savannah (1 full lap)"),
        (4,   "🌳 Walking from St. James to Port of Spain"),
        (6,   "🏙️ Walking from Woodbrook to Diego Martin"),
        (8,   "🏫 Walking from UWI St. Augustine to Curepe"),
        (10,  "🚶 Walking from Port of Spain to Chaguanas"),
        (12,  "🏖️ Walking from Arima to Blanchisseuse"),
        (15,  "🌄 Walking from San Juan to Port of Spain"),
        (18,  "🌊 Walking from Port of Spain to Maracas Bay"),
        (22,  "🏞️ Walking from Arima to Valencia"),
        (25,  "🏖️ Walking from Port of Spain to Las Cuevas"),
        (26.2, "🏃‍♂️ Marathon distance"),
        (35,  "🏭 Walking from Couva to San Fernando"),
        (40,  "🌄 Walking from San Fernando to Port of Spain"),
        (45,  "🌴 Walking from Sangre Grande to Toco"),
        (55,  "🌊 Walking from Mayaro to Sangre Grande"),
        (65,  "🌊 Walking from Point Fortin to San Fernando"),
        (75,  "🌾 Walking from Penal to San Fernando"),
        (85,  "🏝️ Walking from Port of Spain to Toco"),
        (100, "🔥 Walking from Penal to Port of Spain"),
        (120, "🌋 Walking from Point Fortin to Port of Spain"),
        (140, "🗺️ Walking from San Fernando to Toco"),
        (160, "🇹🇹 Walking across Trinidad (Point Fortin → Toco)"),
        (180, "⛴️ Walking Trinidad & Tobago (Point Fortin → Scarborough)"),
        (200, "🏆 Walking Trinidad & Tobago end-to-end challenge"),
        (211, "🚶 Walking from NYC to Boston"),
        (450, "🗽 Walking from NYC to Niagara Falls"),
        (1000, "🌴 Walking from Miami to NYC"),
        (1200, "🏔️ Walking from NYC to Chicago"),
        (2000, "🌉 Walking from NYC to Denver"),
        (2800, "🌊 Walking from NYC to Los Angeles"),
        (3500, "🇺🇸 Walking coast to coast (NYC to LA via southern route)"),
        (5000, "🌍 Walking from NYC to London (if you could!)"),
        (7917, "🌏 Walking around the Earth's circumference at equator") 
    ]
    
    # Find closest comparison
    for distance, description in comparisons:
        if miles < distance:
            progress = (miles / distance) * 100
            return f"{miles:.1f} miles ({km:.1f} km) - {progress:.0f}% of {description}"
    
    # If more than walking around Earth
    times_around = miles / 24901
    return f"{miles:.1f} miles ({km:.1f} km) - {times_around:.1f}x around Earth! 🌍"

def export_data():
    """Export data as JSON"""
    return json.dumps(st.session_state.participants, indent=2)

def import_data(json_str):
    """Import data from JSON"""
    try:
        st.session_state.participants = json.loads(json_str)
        return True
    except:
        return False

# Header
st.title("🏆 3-Month Step Challenge")
st.markdown("**Jan 12 - Apr 12, 2026**")

# Top stats
col1, col2, col3 = st.columns(3)
total_steps = sum(get_participant_stats(n)['total_steps'] for n in st.session_state.participants.keys())
total_weeks = sum(len(d['entries']) for d in st.session_state.participants.values())
avg_weekly = total_steps // total_weeks if total_weeks > 0 else 0

with col1:
    st.metric("Total Steps", f"{total_steps:,}")
with col2:
    st.metric("Avg Weekly Steps", f"{avg_weekly:,}")
with col3:
    st.metric("Participants", len(st.session_state.participants))

# Team distance comparison
if total_steps > 0:
    st.info(f"**🌎 Team Achievement:** {get_distance_comparison(total_steps)}")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Leaderboard", "📊 Analytics", "📝 All Entries", "⚙️ Manage"])

# LEADERBOARD TAB
with tab1:
    st.subheader("Current Standings")
    
    leaderboard = get_leaderboard()
    
    for idx, person in enumerate(leaderboard):
        # Bigger medals for top 3
        if idx == 0:
            medal = "🥇"
            medal_size = "### "
        elif idx == 1:
            medal = "🥈"
            medal_size = "### "
        elif idx == 2:
            medal = "🥉"
            medal_size = "### "
        else:
            medal = f"#{idx + 1}"
            medal_size = "#### "
        
        col1, col2, col3 = st.columns([1, 6, 2])
        with col1:
            st.markdown(f"{medal_size}{medal}")
        with col2:
            st.markdown(f"**{person['name']}**")
            st.caption(f"{person['total_steps']:,} steps • {person['weeks']} weeks • Avg: {person['avg_daily']:,}/day")
            if person['total_steps'] > 0:
                st.caption(f"🗺️ {get_distance_comparison(person['total_steps'])}")
        with col3:
            st.markdown(f"### {person['total_points']:,}")
            st.caption("points")
        st.divider()
    
    # Points system
    with st.expander("📋 Points System"):
        st.markdown("""
        **Per Week:**
        - Base: 1 point per 100 steps
        - 5,000+ steps: +50 bonus
        - 7,500+ steps: +75 bonus
        - 10,000+ steps: +100 bonus
        - 12,500+ steps: +150 bonus
        - 15,000+ steps: +200 bonus
        """)

# ANALYTICS TAB
with tab2:
    st.subheader("Weekly Step Trends")
    
    # Prepare data for weekly trend chart
    all_weeks = set()
    for person_data in st.session_state.participants.values():
        for entry in person_data['entries']:
            all_weeks.add(entry['week_start'])
    
    if all_weeks:
        weeks_sorted = sorted(list(all_weeks))
        
        # Create dataframe for line chart
        trend_data = []
        for week in weeks_sorted:
            week_label = datetime.strptime(week, '%Y-%m-%d').strftime('%b %d')
            for name, data in st.session_state.participants.items():
                entry = next((e for e in data['entries'] if e['week_start'] == week), None)
                if entry:
                    trend_data.append({
                        'Week': week_label,
                        'Participant': name,
                        'Steps': entry['steps']
                    })
        
        if trend_data:
            df_trend = pd.DataFrame(trend_data)
            fig_trend = px.line(df_trend, x='Week', y='Steps', color='Participant', 
                              markers=True, title="Weekly Step Progression")
            st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No data yet. Add some entries to see trends!")
    
    st.subheader("Total Performance Comparison")
    
    # Bar chart for total steps
    leaderboard = get_leaderboard()
    df_total = pd.DataFrame(leaderboard)
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_total['name'],
        y=df_total['total_steps'],
        name='Total Steps',
        marker_color='#3B82F6'
    ))
    fig_bar.add_trace(go.Bar(
        x=df_total['name'],
        y=df_total['avg_daily'],
        name='Avg Daily Steps',
        marker_color='#10B981',
        yaxis='y2'
    ))
    
    fig_bar.update_layout(
        yaxis=dict(title='Total Steps'),
        yaxis2=dict(title='Avg Daily Steps', overlaying='y', side='right'),
        barmode='group'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ALL ENTRIES TAB
with tab3:
    st.subheader("All Weekly Entries")
    
    for name, data in st.session_state.participants.items():
        with st.expander(f"{name} ({len(data['entries'])} weeks)"):
            if data['entries']:
                # Sort by most recent
                sorted_entries = sorted(data['entries'], 
                                      key=lambda x: x['week_start'], 
                                      reverse=True)
                
                for idx, entry in enumerate(sorted_entries):
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.text(f"{entry['week_start']} to {entry['week_end']}")
                    with col2:
                        st.text(f"{entry['steps']:,} steps • {calculate_points(entry['steps']):,} pts")
                    with col3:
                        if st.button("🗑️", key=f"del_{name}_{idx}"):
                            data['entries'].remove(entry)
                            st.rerun()
            else:
                st.info("No entries yet")

# MANAGE TAB
with tab4:
    st.subheader("Add Weekly Entry")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_person = st.selectbox("Participant", list(st.session_state.participants.keys()))
        week_start = st.date_input("Week Start", value=datetime(2026, 1, 12))
    with col2:
        steps = st.number_input("Total Steps for Week", min_value=0, value=0, step=1000)
        week_end = st.date_input("Week End", value=datetime(2026, 1, 18))
    
    if steps > 0:
        st.info(f"Points: {calculate_points(steps):,} • Avg per day: {steps // 7:,}")
    
    if st.button("➕ Add Entry", type="primary"):
        if steps > 0:
            new_entry = {
                'week_start': week_start.strftime('%Y-%m-%d'),
                'week_end': week_end.strftime('%Y-%m-%d'),
                'steps': steps
            }
            st.session_state.participants[selected_person]['entries'].append(new_entry)
            st.success(f"✅ Added {steps:,} steps for {selected_person}")
            st.rerun()
        else:
            st.error("Please enter steps greater than 0")
    
    st.divider()
    
    # Data management
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Export Data**")
        json_data = export_data()
        st.download_button(
            label="📥 Download Backup (JSON)",
            data=json_data,
            file_name=f"step_challenge_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col2:
        st.markdown("**Import Data**")
        uploaded_file = st.file_uploader("Upload JSON backup", type=['json'])
        if uploaded_file is not None:
            json_str = uploaded_file.read().decode()
            if import_data(json_str):
                st.success("✅ Data imported successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid JSON file")
    
    st.divider()
    
    if st.button("🗑️ Clear All Data", type="secondary"):
        if st.checkbox("I confirm I want to delete all data"):
            st.session_state.participants = {
                'Riad': {'color': '#3B82F6', 'entries': []},
                'Keith': {'color': '#10B981', 'entries': []},
                'Hari': {'color': '#F59E0B', 'entries': []},
                'Victoria': {'color': '#EF4444', 'entries': []},
                'Leigeme': {'color': '#8B5CF6', 'entries': []},
                'Derek': {'color': '#EC4899', 'entries': []}
            }
            st.rerun()

# Footer
st.divider()
st.caption("💡 Tip: Check your phone's step counter (iPhone: Health app, Android: Google Fit) and log steps weekly!")