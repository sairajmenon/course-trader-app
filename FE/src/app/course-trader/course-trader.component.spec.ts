import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CourseTraderComponent } from './course-trader.component';

describe('CourseTraderComponent', () => {
  let component: CourseTraderComponent;
  let fixture: ComponentFixture<CourseTraderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CourseTraderComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CourseTraderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
