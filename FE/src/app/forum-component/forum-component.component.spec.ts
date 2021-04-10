import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ForumComponentComponent } from './forum-component.component';

describe('ForumComponentComponent', () => {
  let component: ForumComponentComponent;
  let fixture: ComponentFixture<ForumComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ForumComponentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ForumComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
